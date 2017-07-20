import ObjectsUnification.unification as unification
from unittest import TestCase


class UnificationTest(TestCase):

    def setUp(self):
        self.frames = [
            ['obj11', 'obj12', 'obj13', 'obj14'],
            ['obj21', 'obj22', 'obj23', 'obj24', 'obj25'],
            ['obj31', 'obj32', 'obj33'],
            ['obj41', 'obj42', 'obj43', 'obj44']
        ]

    @staticmethod
    def calculate_similarity(obj1, obj2):
        # connection 1
        if (obj1 == 'obj11' and obj2 == 'obj23') or (obj2 == 'obj11' and obj1 == 'obj23') or \
                (obj1 == 'obj23' and obj2 == 'obj31') or (obj2 == 'obj23' and obj1 == 'obj31') or \
                (obj1 == 'obj31' and obj2 == 'obj41') or (obj2 == 'obj31' and obj1 == 'obj41'):
            return 0.9

        # connection 2
        elif (obj1 == 'obj12' and obj2 == 'obj21') or (obj2 == 'obj12' and obj1 == 'obj21') or \
                (obj1 == 'obj21' and obj2 == 'obj32') or (obj2 == 'obj21' and obj1 == 'obj32') or \
                (obj1 == 'obj32' and obj2 == 'obj42') or (obj2 == 'obj32' and obj1 == 'obj42'):
            return 0.9

        # connection 3
        elif (obj1 == 'obj13' and obj2 == 'obj22') or (obj2 == 'obj13' and obj1 == 'obj22') or \
                (obj1 == 'obj22' and obj2 == 'obj33') or (obj2 == 'obj22' and obj1 == 'obj33') or \
                (obj1 == 'obj33' and obj2 == 'obj43') or (obj2 == 'obj33' and obj1 == 'obj43'):
            return 0.9

        # connection 4
        elif (obj1 == 'obj14' and obj2 == 'obj25') or (obj2 == 'obj14' and obj1 == 'obj25') or \
                (obj1 == 'obj25' and obj2 == 'obj44') or (obj2 == 'obj25' and obj1 == 'obj44'):
            return 0.9

        # relations inside connection 1
        elif (obj1 == 'obj11' and obj2 == 'obj31') or (obj2 == 'obj11' and obj1 == 'obj31'):
            return 0.76
        elif (obj1 == 'obj11' and obj2 == 'obj41') or (obj2 == 'obj11' and obj1 == 'obj41'):
            return 0.87
        elif (obj1 == 'obj23' and obj2 == 'obj41') or (obj2 == 'obj23' and obj1 == 'obj41'):
            return 0.60

        # relations inside connection 2
        elif (obj1 == 'obj12' and obj2 == 'obj32') or (obj2 == 'obj12' and obj1 == 'obj32'):
            return 0.86
        elif (obj1 == 'obj12' and obj2 == 'obj42') or (obj2 == 'obj12' and obj1 == 'obj42'):
            return 0.60
        elif (obj1 == 'obj21' and obj2 == 'obj42') or (obj2 == 'obj21' and obj1 == 'obj42'):
            return 0.74

        # relations inside connection 3
        elif (obj1 == 'obj13' and obj2 == 'obj33') or (obj2 == 'obj13' and obj1 == 'obj33'):
            return 0.85
        elif (obj1 == 'obj13' and obj2 == 'obj43') or (obj2 == 'obj13' and obj1 == 'obj43'):
            return 0.80
        elif (obj1 == 'obj22' and obj2 == 'obj43') or (obj2 == 'obj22' and obj1 == 'obj43'):
            return 0.52

        # relations inside connection 4
        elif (obj1 == 'obj14' and obj2 == 'obj44') or (obj2 == 'obj14' and obj1 == 'obj44'):
            return 0.73

        else:
            return 0.4

    def test_unify_object_should_return_non_empty_list_of_objects(self):
        result = unification.unify_objects(self.frames, self.calculate_similarity)
        objects = [obj[0] for obj in result]
        certainty_factors = [obj[1] for obj in result]

        self.assertTrue('obj31' in objects)
        self.assertAlmostEqual(0.853, certainty_factors[objects.index('obj31')], places=3)

        self.assertTrue('obj32' in objects)
        self.assertAlmostEqual(0.887, certainty_factors[objects.index('obj32')], places=3)

        self.assertTrue('obj33' in objects)
        self.assertAlmostEqual(0.883, certainty_factors[objects.index('obj33')], places=3)

        self.assertTrue('obj25' in objects)
        self.assertAlmostEqual(0.9, certainty_factors[objects.index('obj25')], places=3)


