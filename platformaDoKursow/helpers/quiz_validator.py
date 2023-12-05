from platformaDoKursow.models import Quiz, Answer, Question, Chapter


class QuizValidator:
    def __init__(self, request_data: dict, chapter: Chapter) -> None:
        self.chapter = chapter
        self.request_data = request_data
        self.questions = []
        self.quiz = None
        self.errors = set()

    def is_valid(self) -> bool:
        try:
            self._validate()

        except KeyError:
            self.errors.add('Wrong request structure')
        return False if self.errors else True

    def _validate(self) -> None:
        if len(self.request_data['title']) == 0:
            self.errors.add('Title cannot be empty')

        if not 0 < float(self.request_data['percentage_required']) / 100 < 1:
            self.errors.add('Percentage must be between 0 and 100')

        if len(self.request_data['questions']) < 1:
            self.errors.add('Quiz must have at least one question.')

        if int(self.request_data['allowed_attempts']) < 0:
            self.errors.add('Attempts amount cannot be lower than 0.')

        for question in self.request_data['questions']:
            at_least_one_correct = False
            if len(question['answers']) < 2:
                self.errors.add('Each question must have at least two answers.')

            if len(question['text']) < 10:
                self.errors.add('Question cannot be shorter than 10 characters.')

            if not 0 < int(question['points']) <= 10:
                self.errors.add('Question points should range between 1 and 10.')

            for answer in question['answers']:
                if answer['correct']: at_least_one_correct = True
                if len(answer['text']) == 0:
                    self.errors.add('Answer cannot be empty.')

            if not at_least_one_correct:
                self.errors.add('Each question should have at least one correct answer.')

    def save(self) -> None:
        Quiz.objects.filter(chapter=self.chapter).delete()

        quiz = Quiz(
            chapter=self.chapter,
            title=self.request_data['title'],
            description=self.request_data.get('description'),
            percentage_required=float(self.request_data['percentage_required']) / 100,
            allowed_attempts=self.request_data['allowed_attempts']
        )
        quiz.save()
        answers = []
        for question in self.request_data['questions']:
            question_obj = Question(
                text=question['text'],
                type='text_question',
                points=question['points'],
                partially_accepted=int(question['partially_accepted']),
                quiz=quiz
            )
            question_obj.save()

            answers.extend(
                [
                    Answer(
                        text=answer['text'],
                        is_correct=answer['correct'],
                        question=question_obj
                    ) for answer in question['answers']
                ]
            )
        Answer.objects.bulk_create(answers)
