import random
import unittest

from sentences.generate_text import generate_text


def line_print(long_text, lin_len):
    new = '("' + long_text[:lin_len] + '" +\n'
    long_text = long_text[lin_len:]
    while long_text:
        new += ' "' + long_text[:lin_len] + '" +\n'
        long_text = long_text[lin_len:]
    new = new[:-3] + '),'
    print(new)


def short_line_print(short_text):
    print('"{}",'.format(short_text))


class TestGenerateText(unittest.TestCase):
    def test_default(self):
        random.seed(3)
        present, past = generate_text()

        present_answer = [
            ("<bold>A tree</bold> <bold>catches</bold> a witch<bold>.</bold> <bold>The witch</bold> uses an uncle." +
             " The uncle <bold>draws</bold> a sheep<bold>!</bold> <bold>The sheep</bold> uses a person! <bold>The " +
             "person</bold> doesn't wear them. They wear a pen! The pen arrests a bicycle. The bicycle doesn't ste" +
             "al a baby. <bold>The baby</bold> <bold>doesn't surprise</bold> him. He plays with the pen! The pen t" +
             "akes the person<bold>!</bold> <bold>The person</bold> doesn't teach a car boxes. The boxes catch a f" +
             "ish! The fish interests thunder. The thunder <bold>doesn't hold</bold> the pen! -- error count: 10"),
            ("We freeze an apple! The apple makes apple juice. The apple juice <bold>doesn't give</bold> us rice. " +
             "The rice grabs buses! The buses <bold>don't throw</bold> him. He teaches me watches. The watches bor" +
             "e a fire fighter. The fire fighter pulls a pony. The pony kills <bold>stinky tofu</bold><bold>.</bol" +
             "d> <bold>The stinky tofu</bold> washes you. You don't buy it<bold>.</bold> <bold>It</bold> <bold>doe" +
             "sn't wash</bold> a teacher! The teacher <bold>doesn't kiss</bold> leaves. The leaves grab <bold>a pe" +
             "n</bold>! The pen freezes an egg<bold>.</bold> -- error count: 9"),
            ("You don't interest me<bold>.</bold> <bold>I</bold> bring husbands a school! The school <bold>sleeps<" +
             "/bold> on an ant. The ant gives <bold>a pen</bold> <bold>elephants</bold><bold>!</bold> <bold>The el" +
             "ephants</bold> don't pick up a table. <bold>The table</bold> doesn't catch a bus. The bus loves a bo" +
             "x! <bold>The box</bold> shakes poop<bold>.</bold> <bold>The poop</bold> <bold>steals</bold> hair! Th" +
             "e hair doesn't see sand. The sand doesn't build a nose<bold>!</bold> <bold>The nose</bold> <bold>doe" +
             "sn't own</bold> the bus! The bus doesn't kiss a banana! The banana finds a watch! <bold>The watch</b" +
             "old> <bold>doesn't disgust</bold> milk! -- error count: 13"),
            ("An octopus gets them. They bring an ant homework. The homework bangs me. I bore us. We <bold>don't d" +
             "raw</bold> pizza<bold>.</bold> <bold>The pizza</bold> <bold>gives</bold> the octopus <bold>babies</b" +
             "old>. The babies don't freeze cake. <bold>The cake</bold> brings <bold>eagles</bold> a bus! The bus " +
             "has a tree! <bold>The tree</bold> <bold>surprises</bold> the eagles! The eagles wear tea! The tea do" +
             "esn't grab oranges<bold>.</bold> <bold>The oranges</bold> don't jump on poop! The poop kills <bold>s" +
             "tinky tofu</bold><bold>.</bold> <bold>The stinky tofu</bold> likes a witch<bold>!</bold> -- error co" +
             "unt: 13")
        ]
        present_error = [
            ("Tree catched a witch, the witch uses an uncle. The uncle draweds a sheep, the sheep uses a person! A" +
             " person doesn't wear them. They wear a pen! The pen arrests a bicycle. The bicycle doesn't steal a b" +
             "aby. Babies doesn't surprise him. He plays with the pen! The pen takes the person, the person doesn'" +
             "t teach a car boxes. The boxes catch a fish! The fish interests thunder. The thunder don't hold the " +
             "pen!"),
            ("We freeze an apple! The apple makes apple juice. The apple juice didn't give us rice. The rice grabs" +
             " buses! The buses doesn't throw him. He teaches me watches. The watches bore a fire fighter. The fir" +
             "e fighter pulls a pony. The pony kills a stinky tofu, the stinky tofu washes you. You don't buy it, " +
             "it don't wash a teacher! The teacher didn't kisses leaves. The leaves grab pens! The pen freezes an " +
             "egg,"),
            ("You don't interest me, i bring husbands a school! The school sleep on an ant. The ant gives pens an " +
             "elephant, the elephants don't pick up a table. Table doesn't catch a bus. The bus loves a box! A box" +
             " shakes poop, the poop stealed hair! The hair doesn't see sand. The sand doesn't build a nose, the n" +
             "ose didn't own the bus! The bus doesn't kiss a banana! The banana finds a watch! A watches don't dis" +
             "gust milk!"),
            ("An octopus gets them. They bring an ant homework. The homework bangs me. I bore us. We doesn't draw " +
             "pizza, the pizza give the octopus baby. The babies don't freeze cake. Cakes brings an eagle a bus! T" +
             "he bus has a tree! A tree surprise the eagles! The eagles wear tea! The tea doesn't grab oranges, th" +
             "e orange don't jump on poop! The poop kills a stinky tofu, the stinky tofu likes a witch,")
        ]
        past_answer = [
            ("A tree didn't catch <bold>a witch</bold>. The witch used an uncle. The uncle drew a sheep! The sheep" +
             " didn't use <bold>a person</bold>! The person wore them. They didn't wear <bold>a pen</bold><bold>!<" +
             "/bold> <bold>The pen</bold> <bold>arrested</bold> a bicycle. The bicycle stole a baby<bold>.</bold> " +
             "<bold>The baby</bold> surprised him. He played with the pen! The pen took the person<bold>!</bold> <" +
             "bold>The person</bold> taught a car boxes. <bold>The boxes</bold> caught a fish! <bold>The fish</bol" +
             "d> didn't interest thunder<bold>.</bold> <bold>The thunder</bold> held the pen! -- error count: 10"),
            ("We didn't freeze <bold>an apple</bold>! The apple didn't make <bold>apple juice</bold>. The apple ju" +
             "ice didn't give us <bold>rice</bold>. The rice grabbed <bold>buses</bold>! The buses threw him<bold>" +
             ".</bold> <bold>He</bold> taught me watches. The watches bored a fire fighter. The fire fighter didn'" +
             "t pull a pony. The pony killed stinky tofu. The stinky tofu <bold>washed</bold> you<bold>.</bold> <b" +
             "old>You</bold> bought it. It washed a teacher! The teacher kissed leaves<bold>.</bold> <bold>The lea" +
             "ves</bold> grabbed a pen! The pen didn't freeze an egg<bold>.</bold> -- error count: 9"),
            ("You interested me. I brought <bold>husbands</bold> a school<bold>!</bold> <bold>The school</bold> sl" +
             "ept on an ant. The ant gave a pen elephants<bold>!</bold> <bold>The elephants</bold> picked up a tab" +
             "le. The table caught <bold>a bus</bold>. The bus <bold>didn't love</bold> <bold>a box</bold>! The bo" +
             "x shook poop. The poop stole <bold>hair</bold>! The hair didn't see sand. The sand built <bold>a nos" +
             "e</bold>! The nose <bold>owned</bold> <bold>the bus</bold>! The bus <bold>kissed</bold> a banana! Th" +
             "e banana found a watch! The watch didn't disgust milk<bold>!</bold> -- error count: 14"),
            ("<bold>An octopus</bold> got them. They <bold>brought</bold> <bold>an ant</bold> homework<bold>.</bol" +
             "d> <bold>The homework</bold> banged me. I bored us. We didn't draw pizza. The pizza gave <bold>the o" +
             "ctopus</bold> babies. The babies froze cake. The cake brought eagles <bold>a bus</bold>! The bus did" +
             "n't have a tree! The tree surprised the eagles! The eagles didn't wear tea! The tea didn't grab oran" +
             "ges. The oranges didn't jump on poop! <bold>The poop</bold> killed stinky tofu. The stinky tofu like" +
             "d a witch! -- error count: 7")
        ]
        past_error = [
            ("A tree didn't catch witch. The witch used an uncle. The uncle drew a sheep! The sheep didn't use per" +
             "son! The person wore them. They didn't wear pen, the pen arrests a bicycle. The bicycle stole a baby" +
             ", the baby surprised him. He played with the pen! The pen took the person, the person taught a car b" +
             "oxes. The box caught a fish! Fishes didn't interest thunder, the thunder held the pen!"),
            ("We didn't freeze apple! The apple didn't make apple juices. The apple juice didn't give us a rice. T" +
             "he rice grabbed bus! The buses threw him, he taught me watches. The watches bored a fire fighter. Th" +
             "e fire fighter didn't pull a pony. The pony killed stinky tofu. The stinky tofu washes you, you boug" +
             "ht it. It washed a teacher! The teacher kissed leaves, the leaves grabbed a pen! The pen didn't free" +
             "ze an egg,"),
            ("You interested me. I brought a husbands a school, schools slept on an ant. The ant gave a pen elepha" +
             "nts, elephant picked up a table. The table caught bus. The bus don't love box! The box shook poop. T" +
             "he poop stole hairs! The hair didn't see sand. The sand built noses! The nose own bus! The bus kisse" +
             "s a banana! The banana found a watch! The watch didn't disgust milk,"),
            ("Octopus got them. They brings ant homework, the homework banged me. I bored us. We didn't draw pizza" +
             ". The pizza gave octopuses babies. The babies froze cake. The cake brought eagles bus! The bus didn'" +
             "t have a tree! The tree surprised the eagles! The eagles didn't wear tea! The tea didn't grab orange" +
             "s. The oranges didn't jump on poop! Poops killed stinky tofu. The stinky tofu liked a witch!")
        ]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_paragraph_size(self):
        random.seed(100)
        present, past = generate_text(paragraph_size=2)

        present_answer = [
            "It surprises her<bold>!</bold> <bold>She</bold> doesn't grab sand<bold>.</bold> -- error count: 2",
            "<bold>An elephant</bold> doesn't hit uncles. The uncles take a cow! -- error count: 1",
            "A sheep hits <bold>stinky tofu</bold>. <bold>The stinky tofu</bold> freezes a fish. -- error count: 2",
            ("A bus sleeps on a baby. <bold>The baby</bold> <bold>sleeps</bold> on a person<bold>!</bold> -- error" +
             " count: 3"),
        ]
        present_error = [
            "It surprises her, she doesn't grab sand,",
            "Elephant doesn't hit uncles. The uncles take a cow!",
            "A sheep hits stinky tofus. Stinky tofus freezes a fish.",
            "A bus sleeps on a baby. Baby sleeped on a person,"
        ]
        past_answer = [
            "It surprised her! She didn't grab sand. -- error count: 0",
            "An elephant didn't hit uncles. The uncles didn't take <bold>a cow</bold>! -- error count: 1",
            "<bold>A sheep</bold> hit stinky tofu. The stinky tofu froze a fish. -- error count: 1",
            ("<bold>A bus</bold> slept on <bold>a baby</bold>. <bold>The baby</bold> didn't sleep on a person! -- " +
             "error count: 3"),
        ]
        past_error = [
            "It surprised her! She didn't grab sand.",
            "An elephant didn't hit uncles. The uncles didn't take cow!",
            "Sheep hit stinky tofu. The stinky tofu froze a fish.",
            "Bus slept on baby. Baby didn't sleep on a person!"
        ]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_num_paragraphs(self):
        random.seed(5)
        present, past = generate_text(num_paragraphs=2, paragraph_size=1)

        present_answer = [
            "Money <bold>grabs</bold> tea! -- error count: 1",
            "Milk eats <bold>eagles</bold>. -- error count: 1"
        ]
        present_error = ["Money grabbed tea!", "Milk eats eagle."]
        past_answer = ['Money grabbed <bold>tea</bold><bold>!</bold> -- error count: 2',
                       "Milk <bold>didn't eat</bold> <bold>eagles</bold>. -- error count: 2"]
        past_error = ['Money grabbed a tea,', "Milk don't eat eagle."]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_subject_pool(self):
        random.seed(50)
        present, past = generate_text(num_paragraphs=1, paragraph_size=5, subject_pool=1)

        present_answer = [
            ("A house hates <bold>fire fighters</bold>! The house kills a nose. The house doesn't make homework<bo" +
             "ld>!</bold> <bold>The house</bold> brings octopuses an egg. The house wears a witch! -- error count:" +
             " 2")
        ]
        present_error = [
            ("A house hates the fire fighter! The house kills a nose. The house doesn't make homework, the house b" +
             "rings octopuses an egg. The house wears a witch!")
        ]
        past_answer = [
            ("A house hated fire fighters! The house <bold>killed</bold> a nose. <bold>The house</bold> didn't mak" +
             "e homework! The house brought octopuses an egg. <bold>The house</bold> wore <bold>a witch</bold>! --" +
             " error count: 4")
        ]
        past_error = [
            ("A house hated fire fighters! The house kill a nose. Houses didn't make homework! The house brought o" +
             "ctopuses an egg. House wore witches!")
        ]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_p_pronoun_one(self):
        random.seed(215)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=1.0)

        present_answer = ["She builds him. -- error count: 0"]
        present_error = ["She builds him."]
        past_answer = ["She <bold>built</bold> him. -- error count: 1"]
        past_error = ["She build him."]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_p_pronoun_zero(self):
        random.seed(2000)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0)

        present_answer = ["Poop kills tea. -- error count: 0"]
        present_error = ["Poop kills tea."]
        past_answer = ["Poop didn't kill tea. -- error count: 0"]
        past_error = ["Poop didn't kill tea."]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_p_pronoun_some(self):
        random.seed(2105)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.5)

        present_answer = ["She <bold>uses</bold> <bold>water</bold>. -- error count: 2"]
        present_error = ["She use waters."]
        past_answer = ["She <bold>used</bold> water. -- error count: 1"]
        past_error = ["She uses water."]
        self.assertEqual(present[0], present_answer)
        self.assertEqual(present[1], present_error)
        self.assertEqual(past[0], past_answer)
        self.assertEqual(past[1], past_error)

    def test_p_plural(self):
        empty = 'tests/test_files/empty.csv'
        random.seed(123)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=1.0,
                                      uncountable_file=empty)
        self.assertEqual(present[0][0], "<bold>Books</bold> surprise boxes. -- error count: 1")

        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=0.0,
                                      uncountable_file=empty)
        self.assertEqual(present[0][0], "A box bites a child. -- error count: 0")
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=0.65,
                                      uncountable_file=empty)
        self.assertEqual(present[0][0], "A leaf <bold>arrests</bold> teachers. -- error count: 1")

    def test_p_negative(self):
        random.seed(123)
        present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=1.0)
        self.assertEqual(present[0],
                         ["I don't surprise <bold>a box</bold><bold>.</bold> -- error count: 2",
                          "We <bold>don't have</bold> her! -- error count: 1"])
        self.assertEqual(past[0],
                         ["I didn't surprise a box. -- error count: 0",
                          "We <bold>didn't have</bold> her! -- error count: 1"])

        present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=0.0)
        self.assertEqual(present[0],
                         ['A sheep uses him. -- error count: 0',
                          'Tea kisses <bold>a pineapple</bold>. -- error count: 1'])
        self.assertEqual(past[0],
                         ['A sheep <bold>used</bold> him. -- error count: 1',
                          'Tea kissed <bold>a pineapple</bold>. -- error count: 1'])

        present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=0.5)
        self.assertEqual(present[0],
                         ['An apple draws tea! -- error count: 0', "An eagle doesn't cook schools. -- error count: 0"])
        self.assertEqual(past[0],
                         ['An apple drew <bold>tea</bold>! -- error count: 1',
                          "An eagle <bold>didn't cook</bold> schools. -- error count: 1"])

    def test_p_error(self):
        random.seed(5613)

        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0)
        answer = "<bold>A baby</bold> <bold>brings</bold> them <bold>sand</bold><bold>.</bold> -- error count: 4"
        self.assertEqual(present[0][0], answer)
        self.assertEqual(present[1][0], "Baby bringed them sands,")
        answer = "<bold>A baby</bold> <bold>didn't bring</bold> them <bold>sand</bold><bold>.</bold> -- error count: 4"
        self.assertEqual(past[0][0], answer)
        self.assertEqual(past[1][0], "Baby doesn't bring them a sand,")

        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=0.0)
        self.assertEqual(present[0][0], "You find babies. -- error count: 0")
        self.assertEqual(present[1][0], "You find babies.")
        self.assertEqual(past[0][0], "You found babies. -- error count: 0")
        self.assertEqual(past[1][0], "You found babies.")

        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=0.5)
        self.assertEqual(present[0][0],
                         "He <bold>doesn't wear</bold> <bold>a fire fighter</bold><bold>.</bold> -- error count: 3")
        self.assertEqual(present[1][0], "He don't wear fire fighter,")
        self.assertEqual(past[0][0], "He wore <bold>a fire fighter</bold><bold>.</bold> -- error count: 2")
        self.assertEqual(past[1][0], "He wore fire fighter,")

    def test_noun_errors(self):
        random.seed(4589)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0, p_pronoun=0.0,
                                      noun_errors=True,
                                      verb_errors=False, period_errors=False)
        self.assertEqual(present[0][0], "<bold>Octopuses</bold> freeze <bold>husbands</bold>. -- error count: 2")
        self.assertEqual(present[1][0], "Octopus freeze husband.")
        self.assertEqual(past[0][0], "<bold>Octopuses</bold> froze <bold>husbands</bold>. -- error count: 2")
        self.assertEqual(past[1][0], "The octopus froze a husband.")

    def test_verb_errors(self):
        random.seed(456132)
        present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0, p_pronoun=0.0,
                                      verb_errors=True,
                                      noun_errors=False, period_errors=False)
        self.assertEqual(present[0][0], "Tigers <bold>sell</bold> pineapples! -- error count: 1")
        self.assertEqual(present[1][0], "Tigers sells pineapples!")
        self.assertEqual(past[0][0], "Tigers <bold>didn't sell</bold> pineapples! -- error count: 1")
        self.assertEqual(past[1][0], "Tigers don't sell pineapples!")

    def test_period_errors(self):
        random.seed(4561)
        present, past = generate_text(num_paragraphs=1, paragraph_size=2, p_error=1.0, p_pronoun=0.0,
                                      period_errors=True,
                                      noun_errors=False, verb_errors=False)
        answer = "A table owns hair<bold>.</bold> <bold>The hair</bold> holds a fish<bold>.</bold> -- error count: 2"
        self.assertEqual(present[0][0], answer)
        self.assertEqual(present[1][0], "A table owns hair, the hair holds a fish,")
        answer = ("A table owned hair<bold>.</bold> <bold>The hair</bold> didn't hold a fish<bold>.</bold>" +
                  " -- error count: 2")
        self.assertEqual(past[0][0], answer)
        self.assertEqual(past[1][0], "A table owned hair, the hair didn't hold a fish,")

    def test_verb_file(self):
        random.seed(459821)
        file_name = 'tests/test_files/bring.csv'
        present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, verb_file=file_name)
        brings = ['Witches bring husbands sand.', 'We bring husbands homework!', 'We bring gold eggs.',
                  'Cows bring stinky tofu bananas!', "Stinky tofu doesn't bring tea boxes."]
        broughts = ['Witches brought husbands sand.', 'We brought husbands homework!', "We didn't bring gold eggs.",
                    'Cows brought stinky tofu bananas!', "Stinky tofu didn't bring tea boxes."]
        self.assertEqual(present[1], brings)
        self.assertEqual(past[1], broughts)

    def test_countable_file(self):
        random.seed(9871)
        file_name = 'tests/test_files/two_nouns.csv'
        empty = 'tests/test_files/empty.csv'
        present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, p_pronoun=0.0,
                                      countable_file=file_name, uncountable_file=empty)
        self.assertEqual(present[1],
                         ['A bob arrests a joe.', "A joe doesn't bang a bob.", "A bob doesn't freeze joes!",
                          "Bobs don't hold joes.", "A bob doesn't kick a joe."])

    def test_uncountable_file(self):
        random.seed(4591)
        file_name = 'tests/test_files/two_nouns.csv'
        empty = 'tests/test_files/empty.csv'
        present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, p_pronoun=0.0,
                                      countable_file=empty, uncountable_file=file_name)
        # Uncountable nouns don't "s", "a", "an"
        self.assertEqual(present[1],
                         ["Joe doesn't wear bob.", "Joe doesn't find bob.", 'Bob bores joe.', 'Joe bores bob.',
                          'Joe excites bob.'])
