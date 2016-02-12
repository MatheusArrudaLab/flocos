from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

from common.flow_factors import FlowFactors
from .tasks_difficulty import TasksDifficultyModel
from .practice_session import PracticeSession
from django.db.models import Min


def calculate_initial_skill():
    difficulty_of_easiest_task = TasksDifficultyModel.objects.all().aggregate(Min('programming'))['programming__min']
    if difficulty_of_easiest_task is None:
        return Decimal(-1)
    return difficulty_of_easiest_task


class StudentModel(models.Model):
    """Model for a student

       The student model keeps track of the current practice session.
       For every concept there is number between -1 and 1 representing skill in
       certain concept.
    """

    # current session
    session = models.OneToOneField(PracticeSession, null=True, blank=True)

    # init values
    INITIAL_CONCEPT_SKILL = Decimal(-1)

    # student to refer with foreign key
    user = models.OneToOneField(User, primary_key=True)

    # programming concept difficulty
    programming = models.DecimalField(max_digits=4, decimal_places=3,
            default=calculate_initial_skill,
            verbose_name="General skill")

    # conditions concept difficulty
    conditions = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in conditions concept")

    # loops concept difficulty
    loops = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in loops concept")

    # logic expressions concept difficulty
    logic_expr = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in logic expressions concept")

    # colors concept difficulty
    colors = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in colors concept")

    # tokens concept difficulty
    tokens = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in tokens concept")

    # pits concept difficulty
    pits = models.DecimalField(max_digits=4, decimal_places=3,
            default=INITIAL_CONCEPT_SKILL,
            verbose_name="Skill in pits concept")

    def get_skill_dict(self):
        """Return dictionary of skill factors for the student

        Factor values interpretation:
        ~ -1 - the factor is not learnt yet
        ~  0 - the factor is ready to learn
        ~ +1 - the factor is already mastered
        """
        skill_dict = {
            FlowFactors.STUDENT_BIAS: float(self.programming),
            FlowFactors.LOOPS: float(self.loops),
            FlowFactors.CONDITIONS: float(self.conditions),
            FlowFactors.LOGIC_EXPR: float(self.logic_expr),
            FlowFactors.COLORS: float(self.colors),
            FlowFactors.TOKENS: float(self.tokens),
            FlowFactors.PITS: float(self.pits)
        }
        return skill_dict

    def __str__(self):
        skill_dict = self.get_skill_dict()
        skills = [str(skill_dict[factor]) for factor in FlowFactors.student_factors()]
        return 'student={student}, skill=({skills})'.format(
            student=self.student.pk,
            skills=','.join(skills))