import logging
import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View

logger = logging.getLogger(__name__)
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from accounts.decorators import lecturer_required
from accounts.models import Student
from result.models import TakenCourse
from .forms import (
    EssayForm,
    MCQuestionForm,
    MCQuestionFormSet,
    QuestionForm,
    QuizAddForm,
)
from .models import (
    Course,
    EssayQuestion,
    MCQuestion,
    Progress,
    Question,
    Quiz,
    Sitting,
    Choice,
)
from .ai_generator import AIQuestionGenerator


# ########################################################
# Quiz Views
# ########################################################


@method_decorator([login_required, lecturer_required], name="dispatch")
class QuizCreateView(CreateView):
    model = Quiz
    form_class = QuizAddForm
    template_name = "quiz/quiz_form.html"

    def get_initial(self):
        initial = super().get_initial()
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        initial["course"] = course
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, slug=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        form.instance.course = get_object_or_404(Course, slug=self.kwargs["slug"])
        with transaction.atomic():
            self.object = form.save()
            return redirect(
                "mc_create", slug=self.kwargs["slug"], quiz_id=self.object.id
            )


@method_decorator([login_required, lecturer_required], name="dispatch")
class QuizUpdateView(UpdateView):
    model = Quiz
    form_class = QuizAddForm
    template_name = "quiz/quiz_form.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, slug=self.kwargs["slug"])
        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save()
            return redirect("quiz_index", self.kwargs["slug"])


@login_required
@lecturer_required
def quiz_delete(request, slug, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    quiz.delete()
    messages.success(request, "Quiz successfully deleted.")
    return redirect("quiz_index", slug=slug)


@login_required
def quiz_list(request, slug):
    course = get_object_or_404(Course, slug=slug)
    quizzes = Quiz.objects.filter(course=course).order_by("-timestamp")

    context = {
        "quizzes": quizzes,
        "course": course,
    }

    return render(request, "quiz/quiz_list.html", context)


@method_decorator([login_required], name="dispatch")
class QuizWithAIGeneratorView(DetailView):
    """Display quiz with embedded AI question generator"""

    model = Quiz
    template_name = "quiz/quiz_with_ai.html"
    context_object_name = "quiz"

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz, pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.object

        # Get existing questions count
        context["question_count"] = quiz.get_questions().count()

        # AI configuration
        context["ai_models"] = settings.AI_MODELS
        context["default_ai_model"] = settings.DEFAULT_AI_MODEL
        context["default_question_count"] = settings.DEFAULT_AI_QUESTION_COUNT

        # Course info
        context["course"] = quiz.course

        return context


@method_decorator([login_required], name="dispatch")
class AIQuestionGeneratorView(View):
    """Handle AI question generation requests"""

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            topic = data.get("topic", "").strip()
            difficulty = data.get("difficulty", "medium")
            num_questions = min(int(data.get("num_questions", 5)), 20)  # Max 20
            model = data.get("model", "grok")
            quiz_id = data.get("quiz_id")

            if not topic:
                return JsonResponse(
                    {"success": False, "error": "Please enter a topic for question generation."},
                    status=400,
                )

            # Get the appropriate API key
            api_key = settings.OPENROUTER_API_KEY

            # Initialize generator
            generator = AIQuestionGenerator(api_key=api_key, model=model)

            # Generate questions
            questions = generator.generate_questions(
                topic=topic, difficulty=difficulty, num_questions=num_questions
            )

            # Get quiz info if provided
            quiz_info = {}
            if quiz_id:
                try:
                    quiz = Quiz.objects.get(id=quiz_id)
                    quiz_info = {
                        "id": quiz.id,
                        "title": quiz.title,
                        "slug": quiz.slug,
                        "course": {
                            "id": quiz.course.id,
                            "title": quiz.course.title,
                            "slug": quiz.course.slug,
                        },
                    }
                except Quiz.DoesNotExist:
                    pass

            return JsonResponse(
                {
                    "success": True,
                    "questions": questions,
                    "count": len(questions),
                    "model_used": model,
                    "difficulty": difficulty,
                    "quiz": quiz_info,
                    "generated_at": timezone.now().isoformat(),
                }
            )

        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return JsonResponse(
                {"success": False, "error": "Invalid input parameters."}, status=400
            )
        except Exception as e:
            logger.error(f"AI generation error: {str(e)}")
            return JsonResponse(
                {
                    "success": False,
                    "error": f"Failed to generate questions: {str(e)}",
                    "fallback": True,
                },
                status=500,
            )


@login_required
def save_ai_questions(request, quiz_id):
    """Save AI-generated questions to the quiz"""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    try:
        quiz = get_object_or_404(Quiz, id=quiz_id)

        # Check permission
        if not (request.user.is_superuser or request.user.is_lecturer):
            return JsonResponse(
                {
                    "error": "You do not have permission to add questions to this quiz."
                },
                status=403,
            )

        data = json.loads(request.body)
        questions_data = data.get("questions", [])

        if not questions_data:
            return JsonResponse(
                {"success": False, "error": "No questions provided."}, status=400
            )

        created_questions = []

        with transaction.atomic():
            for q_data in questions_data:
                # Create MCQuestion
                mc_question = MCQuestion.objects.create(
                    content=q_data["content"],
                    explanation=q_data.get("explanation", "Generated by AI"),
                    choice_order="random",
                    figure=None,
                )

                # Add to quiz
                mc_question.quiz.add(quiz)

                # Create choices
                for choice_data in q_data["choices"]:
                    Choice.objects.create(
                        question=mc_question,
                        choice_text=choice_data["text"],
                        correct=(
                            choice_data["letter"].upper() == q_data["correct"].upper()
                        ),
                    )

                created_questions.append(
                    {"id": mc_question.id, "content": mc_question.content}
                )

        logger.info(
            f"User {request.user} saved {len(created_questions)} AI questions to quiz {quiz_id}"
        )

        return JsonResponse(
            {
                "success": True,
                "message": f"Successfully added {len(created_questions)} questions to the quiz.",
                "added_count": len(created_questions),
                "questions": created_questions,
            }
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        logger.error(f"Failed to save AI questions: {str(e)}")
        return JsonResponse(
            {"success": False, "error": f"Failed to save questions: {str(e)}"},
            status=500,
        )


# ########################################################
# Multiple Choice Question Views
# ########################################################


@method_decorator([login_required, lecturer_required], name="dispatch")
class MCQuestionCreate(CreateView):
    model = MCQuestion
    form_class = MCQuestionForm
    template_name = "quiz/mcquestion_form.html"

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs["quiz"] = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, slug=self.kwargs["slug"])
        context["quiz_obj"] = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])
        context["quiz_questions_count"] = Question.objects.filter(
            quiz=self.kwargs["quiz_id"]
        ).count()
        if self.request.method == "POST":
            context["formset"] = MCQuestionFormSet(self.request.POST)
        else:
            context["formset"] = MCQuestionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            with transaction.atomic():
                # Save the MCQuestion instance without committing to the database yet
                self.object = form.save(commit=False)
                self.object.save()

                # Retrieve the Quiz instance
                quiz = get_object_or_404(Quiz, id=self.kwargs["quiz_id"])

                # set the many-to-many relationship
                self.object.quiz.add(quiz)

                # Save the formset (choices for the question)
                formset.instance = self.object
                formset.save()

                if "another" in self.request.POST:
                    return redirect(
                        "mc_create",
                        slug=self.kwargs["slug"],
                        quiz_id=self.kwargs["quiz_id"],
                    )
                return redirect("quiz_index", slug=self.kwargs["slug"])
        else:
            return self.form_invalid(form)


# ########################################################
# Quiz Progress and Marking Views
# ########################################################


@method_decorator([login_required], name="dispatch")
class QuizUserProgressView(TemplateView):
    template_name = "quiz/progress.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        progress, _ = Progress.objects.get_or_create(user=self.request.user)
        context["cat_scores"] = progress.list_all_cat_scores
        context["exams"] = progress.show_exams()
        context["exams_counter"] = context["exams"].count()
        return context


@method_decorator([login_required, lecturer_required], name="dispatch")
class QuizMarkingList(ListView):
    model = Sitting
    template_name = "quiz/quiz_marking_list.html"

    def get_queryset(self):
        queryset = Sitting.objects.filter(complete=True)
        if not self.request.user.is_superuser:
            queryset = queryset.filter(
                quiz__course__allocated_course__lecturer__pk=self.request.user.id
            )
        quiz_filter = self.request.GET.get("quiz_filter")
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)
        user_filter = self.request.GET.get("user_filter")
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)
        return queryset


@method_decorator([login_required, lecturer_required], name="dispatch")
class QuizMarkingDetail(DetailView):
    model = Sitting
    template_name = "quiz/quiz_marking_detail.html"

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()
        question_id = request.POST.get("qid")
        if question_id:
            question = Question.objects.get_subclass(id=int(question_id))
            if isinstance(question, EssayQuestion):
                score = request.POST.get("score")
                if score is not None:
                    progress = Progress.objects.get(user=sitting.user)
                    progress.update_score(question, int(score), 1)
            else:
                if int(question_id) in sitting.get_incorrect_questions:
                    sitting.remove_incorrect_question(question)
                else:
                    sitting.add_incorrect_question(question)

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = self.object.get_questions(with_answers=True)
        return context


# ########################################################
# Quiz Taking View
# ########################################################


@method_decorator([login_required], name="dispatch")
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = "quiz/question.html"
    result_template_name = "quiz/result.html"

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, slug=self.kwargs["slug"])
        self.course = get_object_or_404(Course, pk=self.kwargs["pk"])
        if not Question.objects.filter(quiz=self.quiz).exists():
            messages.warning(request, "This quiz has no questions available.")
            return redirect("quiz_index", slug=self.course.slug)

        self.sitting = Sitting.objects.user_sitting(
            request.user, self.quiz, self.course
        )
        if not self.sitting:
            messages.info(
                request,
                "You have already completed this quiz. Only one attempt is permitted.",
            )
            return redirect("quiz_index", slug=self.course.slug)

        # Set self.question and self.progress here
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["question"] = self.question
        return kwargs

    def get_form_class(self):
        if isinstance(self.question, EssayQuestion):
            return EssayForm
        return self.form_class

    def form_valid(self, form):
        self.form_valid_user(form)
        if not self.sitting.get_first_question():
            return self.final_result_user()
        return super().get(self.request)

    # Update the form_valid_user method in the QuizTake class
    def form_valid_user(self, form):
        progress, _ = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data["answers"]
        is_correct = False  # Default for essay questions

        if isinstance(self.question, EssayQuestion):
            # Essay questions: record answer but don't auto-score
            progress.update_score(self.question, 0, 1)  # 0 points initially
        else:
            # Handle MCQuestions normally
            is_correct = self.question.check_if_correct(guess)
            if is_correct:
                self.sitting.add_to_score(1)
                progress.update_score(self.question, 1, 1)
            else:
                self.sitting.add_incorrect_question(self.question)
                progress.update_score(self.question, 0, 1)

        # Handle previous question data
        if not self.quiz.answers_at_end:
            self.previous = {
                "previous_answer": guess,
                "previous_outcome": (
                    is_correct if not isinstance(self.question, EssayQuestion) else None
                ),
                "previous_question": self.question,
                "answers": (
                    self.question.get_choices()
                    if not isinstance(self.question, EssayQuestion)
                    else []
                ),
                "question_type": {self.question.__class__.__name__: True},
            }
        else:
            self.previous = {}

        # Store user response and remove the question from the queue
        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

        # Update for next question
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = self.question
        context["quiz"] = self.quiz
        context["course"] = self.course
        if hasattr(self, "previous"):
            context["previous"] = self.previous
        if hasattr(self, "progress"):
            context["progress"] = self.progress
        return context

    def final_result_user(self):
        self.sitting.mark_quiz_complete()

        # Update student's course progress with quiz score
        try:
            student_instance = self.request.user.student
            taken_course, created = TakenCourse.objects.get_or_create(
                student=student_instance,
                course=self.course,
                defaults={'quiz': 0}
            )
            # Update the quiz field with the percentage score
            taken_course.quiz = self.sitting.get_percent_correct
            taken_course.save()
        except (AttributeError, Student.DoesNotExist, Exception) as e:
            # Log error but don't fail quiz completion
            logger.error(f"Failed to update TakenCourse.quiz for user {self.request.user}: {e}")

        results = {
            "course": self.course,
            "quiz": self.quiz,
            "score": self.sitting.get_current_score,
            "max_score": self.sitting.get_max_score,
            "percent": self.sitting.get_percent_correct,
            "sitting": self.sitting,
            "previous": getattr(self, "previous", {}),
        }

        if self.quiz.answers_at_end:
            results["questions"] = self.sitting.get_questions(with_answers=True)
            results["incorrect_questions"] = self.sitting.get_incorrect_questions

        # Keep sitting for students to view their quiz results in progress
        # Delete only for lecturers/supersusers if it's a practice exam_paper
        if self.quiz.exam_paper and (self.request.user.is_superuser or self.request.user.is_lecturer):
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)
