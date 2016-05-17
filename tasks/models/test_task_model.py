"""Unit test of task model
"""

from django.test import TestCase
from .task import TaskModel
from concepts.models import Concept


class TaskModelTest(TestCase):

    fixtures = ['blocks', 'toolboxes', 'concepts', 'tasks']

    def test_concepts_inference_task_54(self):
        task54 = TaskModel.objects.get(pk=54)
        inferred_concepts = task54.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['env-maze', 'env-toolbox',
                                             'env-workspace', 'env-snapping',
                                             'env-run-reset',
                                             'game-block-limit', 'game-tokens',
                                             'block-move', 'block-turn',
                                             'block-repeat', 'block-while',
                                             'block-check-goal',
                                             'programming-sequence',
                                             'programming-repeat',
                                             'programming-while',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_task_36(self):
        task36 = TaskModel.objects.get(pk=36)
        inferred_concepts = task36.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['env-maze', 'env-toolbox',
                                             'env-workspace', 'env-snapping',
                                             'env-run-reset',
                                             'game-block-limit', 'game-colors',
                                             'block-move', 'block-turn',
                                             'block-while', 'block-check-goal',
                                             'block-check-color', 'block-check-path',
                                             'block-if', 'block-logic',
                                             'programming-sequence',
                                             'programming-while',
                                             'programming-if',
                                             'programming-logic',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)


    def test_concepts_inference_no_game_concepts(self):
        task = TaskModel.objects.get(pk=1)
        inferred_concepts = task.get_contained_concepts()
        expected_concepts = set([Concept.objects.get_by_natural_key(key)
                                 for key in ['env-maze', 'env-toolbox',
                                             'env-workspace', 'env-snapping',
                                             'env-run-reset',
                                             'block-move',
                                             'programming-sequence',
                                             ]])
        self.assertSetEqual(inferred_concepts, expected_concepts)

    def test_concepts_inference_colors(self):
        task = TaskModel.objects.get(pk=33)
        inferred_concepts = task.get_contained_concepts()
        colors_concept = Concept.objects.get_by_natural_key('game-colors')
        self.assertIn(colors_concept, inferred_concepts)

    def test_concepts_inference_pits(self):
        task = TaskModel.objects.get(pk=43)
        inferred_concepts = task.get_contained_concepts()
        pits_concept = Concept.objects.get_by_natural_key('game-pits')
        self.assertIn(pits_concept, inferred_concepts)

    def test_blocks_limit_inference(self):
        self.assertEquals(TaskModel.objects.get(pk=1).get_blocks_limit(), None)
        self.assertEquals(TaskModel.objects.get(pk=11).get_blocks_limit(), 7)
