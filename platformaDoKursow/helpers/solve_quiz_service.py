from django.db.models import QuerySet, Count, Prefetch
from platformaDoKursow.models import Quiz, Question, Answer, QuizAttempt


class SolveQuizServiceError(Exception): ...


class SolveQuizService:
    def __init__(self, quiz: Quiz, user, course, request_data) -> None:
        self.quiz = quiz
        self.request_data = request_data
        self.user = user
        self.course = course

    def run(self) -> None:
        all_questions = self._get_all_quiz_questions()
        points = 0
        all_possible_points = sum(question.points for question in all_questions.values())
        for answered_question in self.request_data:
            try:
                question = all_questions[answered_question['question_id']]
                points += self._check_percentage_of_succeed_question(
                    question, answered_question['selected_answers']) * question.points
            except KeyError:
                raise SolveQuizServiceError('Wrong data was sent.')

        quiz_attempt = QuizAttempt(
            user=self.user, quiz=self.quiz, course=self.course,
            points=round(points, 1), percentage=round(points / all_possible_points, 2)
        )
        quiz_attempt.quiz_passed = True if quiz_attempt.percentage >= self.quiz.percentage_required else False
        quiz_attempt.save()

    def _check_percentage_of_succeed_question(self, question: Question, answers_given: list[int]) -> float:
        all_answers = {answer.pk: answer.is_correct for answer in question.answers.all()}
        correct_answers_count = len([answer for answer in question.answers.all() if answer.is_correct])
        answers = {'correct': 0, 'wrong': 0}
        for answer_id in answers_given:
            if all_answers[answer_id]:
                answers['correct'] += 1
            else:
                answers['wrong'] += 1

        if correct_answers_count == answers['correct'] and answers['wrong'] == 0:
            return 1
        elif not question.partially_accepted or answers['correct'] == 0 or correct_answers_count == len(answers_given):
            return 0

        return percent if (percent := ((answers['correct'] - answers['wrong']) / correct_answers_count)) > 0 else 0

    def _get_all_quiz_questions(self) -> dict[int, Question]:
        return {
            question.pk: question
            for question in Question.objects.filter(quiz=self.quiz).prefetch_related('answers')
        }
