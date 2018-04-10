from big_ol_pile_of_manim_imports import *

NAME_WITH_SPACES = "Prime Meridian"
DIAMETER = 5.0
RADIUS = DIAMETER / 2
LETTER_SCALE = 1
THANK_YOU_SCALE = 2

OUTER_RADIUS = RADIUS
INNER_RADIUS = 1.0 * OUTER_RADIUS



class NameAnimationScene(Scene):

    def construct(self):

        name = ''.join(NAME_WITH_SPACES.split(' '))
        letters = list(name)
        nb_letters = len(letters)
        randy = PiCreature()
        randy.move_to(ORIGIN).scale_to_fit_height(0.5 * DIAMETER)
        randy.set_color(BLUE_E)
        randy.look_at(UP + RIGHT)
        randy.change_mode("happy")
        self.add(randy)
        dtheta = TAU/nb_letters
        angles = np.arange(TAU/4,-3 * TAU / 4,-dtheta)
        dr = (OUTER_RADIUS - INNER_RADIUS) / nb_letters
        if dr != 0:
            radii = np.arange(OUTER_RADIUS, INNER_RADIUS, -dr)
        else:
            radii = OUTER_RADIUS * np.ones(nb_letters)
        name_mob = VGroup()
        for (letter, angle, r) in zip(letters, angles, radii):
            letter_mob = TextMobject(letter).scale(LETTER_SCALE)
            pos = r * np.cos(angle) * RIGHT + r * np.sin(angle) * UP
            letter_mob.move_to(pos)
            name_mob.add(letter_mob)

        second_letter = name_mob.submobjects[1]

        self.play(
            LaggedStart(Write, name_mob, run_time = 3),
            ApplyMethod(randy.look_at, second_letter, run_time = 3)
        )

        for i in range(2,nb_letters + 2):

            group = []

            for (j,letter_mob) in enumerate(name_mob.submobjects):

                new_angle = TAU / 4 - i * j * dtheta
                r = radii[j]
                new_pos = r * np.cos(new_angle) * RIGHT + r * np.sin(new_angle) * UP
                letter_mob.target = letter_mob.copy().move_to(new_pos)
                anim = MoveToTarget(letter_mob, path_arc = - j * dtheta)
                group.append(anim)

            self.play(
                AnimationGroup(*group, run_time = 3),
                ApplyMethod(randy.look_at,second_letter, run_time = 3)
            )
            self.wait(0.5)


        thank_you = VGroup(TextMobject("Thank You!"))
        thank_you.scale(THANK_YOU_SCALE).next_to(randy, DOWN)
        new_randy = randy.copy()
        new_randy.change("hooray")
       # new_randy.set_color(BLUE_E)
        new_randy.look_at(ORIGIN)
        self.play(
            Transform(name_mob, thank_you),
            Transform(randy, new_randy)
        )












