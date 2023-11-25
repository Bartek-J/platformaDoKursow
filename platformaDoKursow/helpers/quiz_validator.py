from platformaDoKursow.models import Quiz, Answer, Question


class QuizValidator:
    def __init__(self, request_data) -> None:
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
        if len(self.request_data['questions']) < 1:
            self.errors.add('Quiz must have at least one question.')

        for question in self.request_data['questions']:
            at_least_one_correct = False
            if len(question['answers']) < 2:
                self.errors.add('Each question must have at least two answers.')

            if len(question['text']) < 10:
                self.errors.add('Question cannot be shorter than 10 characters.')

            for answer in question['answers']:
                if answer['is_correct']: at_least_one_correct = True
                if len(answer['text']) == 0:
                    self.errors.add('Answer cannot be empty.')

            if not at_least_one_correct:
                self.errors.add('Question should have at least one correct answer.')





    def save(self) -> None:
        answers = []
        for question in self.request_data['questions']:
            question = Question(text=question['text'])
            question.save()

            answers.extend(
                [
                    Answer(
                        text=answer['text'],
                        is_correct=answer['is_correct'],
                        question=question
                    ) for answer in question['answers']
                ]
            )
        Answer.objects.bulk_create(answers)
