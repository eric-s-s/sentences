# import random
# import unittest
#
# from sentences.generate_text import generate_text
#
#
# def line_print(long_text, lin_len):
#     new = '("' + long_text[:lin_len] + '" +\n'
#     long_text = long_text[lin_len:]
#     while long_text:
#         new += ' "' + long_text[:lin_len] + '" +\n'
#         long_text = long_text[lin_len:]
#     new = new[:-3] + '),'
#     print(new)
#
#
# def short_line_print(short_text):
#     print('"{}",'.format(short_text))
#
#
# class TestGenerateText(unittest.TestCase):
#     def test_default(self):
#         random.seed(3)
#         present, past = generate_text()
#
#         present_answer = [
#             ("<bold>A tree</bold> <bold>buys</bold> witches<bold>.</bold> <bold>The witches</bold> throw fish at a" +
#              "n egg! The egg interests <bold>an uncle</bold>. The uncle hates a child. The child <bold>doesn't own" +
#              "</bold> us. We sell me. I don't sell a baby to an apple. The apple interests a pen! The pen shows pe" +
#              "ople a watch. The watch doesn't wear an orange. The orange bites him<bold>.</bold> <bold>He</bold> w" +
#              "ears <bold>poop</bold>! The poop <bold>surprises</bold> a teacher<bold>.</bold> <bold>The teacher</b" +
#              "old> loves wives. The wives <bold>make</bold> <bold>noses</bold>! -- error count: 11"),
#             ("<bold>Sand</bold> <bold>shows</bold> him a tree. The tree cooks a house. The house smells a table! <" +
#              "bold>The table</bold> doesn't love a banana. The banana eats a tiger<bold>!</bold> <bold>The tiger</" +
#              "bold> hits her. She doesn't surprise you<bold>.</bold> <bold>You</bold> <bold>build</bold> it. It <b" +
#              "old>surprises</bold> a teacher! <bold>The teacher</bold> jumps on a leaf. The leaf gets <bold>a pen<" +
#              "/bold><bold>!</bold> <bold>The pen</bold> fights <bold>an egg</bold>. The egg hits us. We ride <bold" +
#              ">rice</bold>. The rice doesn't love her. -- error count: 12"),
#             ("He steals a baby. The baby hits homework with <bold>an apple</bold>. The apple doesn't freeze a tabl" +
#              "e. The table doesn't disgust <bold>money</bold>. The money doesn't hate her. She <bold>doesn't teach" +
#              "</bold> hair a school! The school throws a tiger at oranges! The oranges don't shake the school<bold" +
#              ">.</bold> <bold>The school</bold> plays with gold. The gold brings a nose to a tree! <bold>The tree<" +
#              "/bold> <bold>builds</bold> a teacher. <bold>The teacher</bold> <bold>bores</bold> the homework<bold>" +
#              "!</bold> <bold>The homework</bold> loves <bold>the gold</bold>! <bold>The gold</bold> sees eagles<bo" +
#              "ld>.</bold> <bold>The eagles</bold> <bold>don't teach</bold> <bold>sharks</bold> an uncle. -- error " +
#              "count: 15"),
#             ("Cake doesn't wash a husband. The husband surprises a teacher. The teacher doesn't like homework. <bo" +
#              "ld>The homework</bold> doesn't cut water! The water doesn't grab <bold>an uncle</bold>. <bold>The un" +
#              "cle</bold> uses her. She draws ice cream. The ice cream gets a cow! The cow sees <bold>lightning</bo" +
#              "ld><bold>!</bold> <bold>The lightning</bold> grabs babies<bold>.</bold> <bold>The babies</bold> <bol" +
#              "d>cook</bold> an apple. <bold>The apple</bold> brings the homework a leaf<bold>.</bold> <bold>The le" +
#              "af</bold> makes gold out of apple juice. The apple juice hits the water with a nose. The nose doesn'" +
#              "t arrest her. -- error count: 10")
#         ]
#         present_error = [
#             ("A trees buy witches, the witches throw fish at an egg! The egg interests uncles. The uncle hates a c" +
#              "hild. The child didn't owns us. We sell me. I don't sell a baby to an apple. The apple interests a p" +
#              "en! The pen shows people a watch. The watch doesn't wear an orange. The orange bites him, he wears p" +
#              "oops! The poop surpriseds a teacher, the teacher loves wives. The wives makes nose!"),
#             ("A sand show him a tree. The tree cooks a house. The house smells a table! Table doesn't love a banan" +
#              "a. The banana eats a tiger, the tiger hits her. She doesn't surprise you, you builds it. It surprise" +
#              "ds a teacher! Teachers jumps on a leaf. The leaf gets pen, the pen fights egg. The egg hits us. We r" +
#              "ide a rice. The rice doesn't love her."),
#             ("He steals a baby. The baby hits homework with apple. The apple doesn't freeze a table. The table doe" +
#              "sn't disgust moneys. The money doesn't hate her. She don't teach hair a school! The school throws a " +
#              "tiger at oranges! The oranges don't shake the school, the school plays with gold. The gold brings a " +
#              "nose to a tree! A trees build a teacher. A teachers bored the homework, a homework loves golds! Gold" +
#              "s sees eagles, the eagles doesn't teach shark an uncle."),
#             ("Cake doesn't wash a husband. The husband surprises a teacher. The teacher doesn't like homework. A h" +
#              "omework doesn't cut water! The water doesn't grab uncle. Uncle uses her. She draws ice cream. The ic" +
#              "e cream gets a cow! The cow sees a lightning, the lightning grabs babies, baby cook an apple. Apple " +
#              "brings the homework a leaf, the leaf makes gold out of apple juice. The apple juice hits the water w" +
#              "ith a nose. The nose doesn't arrest her.")
#         ]
#         past_answer = [
#             ("A tree bought <bold>witches</bold><bold>.</bold> <bold>The witches</bold> didn't throw fish at an eg" +
#              "g! The egg didn't interest an uncle. The uncle didn't hate a child<bold>.</bold> <bold>The child</bo" +
#              "ld> didn't own us. We didn't sell me<bold>.</bold> <bold>I</bold> <bold>sold</bold> a baby to an app" +
#              "le. The apple <bold>interested</bold> <bold>a pen</bold>! The pen showed <bold>people</bold> a watch" +
#              "<bold>.</bold> <bold>The watch</bold> didn't wear an orange. <bold>The orange</bold> didn't bite him" +
#              "<bold>.</bold> <bold>He</bold> wore poop! <bold>The poop</bold> surprised a teacher<bold>.</bold> <b" +
#              "old>The teacher</bold> loved wives<bold>.</bold> <bold>The wives</bold> made noses! -- error count: " +
#              "14"),
#             ("<bold>Sand</bold> showed him a tree<bold>.</bold> <bold>The tree</bold> didn't cook a house. The hou" +
#              "se smelled a table! The table loved a banana. The banana ate a tiger! The tiger <bold>hit</bold> her" +
#              "<bold>.</bold> <bold>She</bold> surprised you. You built it. It surprised a teacher<bold>!</bold> <b" +
#              "old>The teacher</bold> didn't jump on a leaf. The leaf got a pen<bold>!</bold> <bold>The pen</bold> " +
#              "didn't fight an egg<bold>.</bold> <bold>The egg</bold> didn't hit us<bold>.</bold> <bold>We</bold> r" +
#              "ode <bold>rice</bold><bold>.</bold> <bold>The rice</bold> didn't love her. -- error count: 10"),
#             ("He stole <bold>a baby</bold><bold>.</bold> <bold>The baby</bold> <bold>hit</bold> homework with an a" +
#              "pple. <bold>The apple</bold> didn't freeze a table<bold>.</bold> <bold>The table</bold> disgusted mo" +
#              "ney. <bold>The money</bold> <bold>hated</bold> her. She taught hair a school<bold>!</bold> <bold>The" +
#              " school</bold> <bold>threw</bold> a tiger at oranges! The oranges <bold>didn't shake</bold> the scho" +
#              "ol. The school played with gold. <bold>The gold</bold> brought a nose to a tree! The tree <bold>buil" +
#              "t</bold> a teacher. The teacher bored <bold>the homework</bold>! The homework loved the gold! <bold>" +
#              "The gold</bold> <bold>didn't see</bold> eagles. The eagles taught <bold>sharks</bold> an uncle. -- e" +
#              "rror count: 16"),
#             ("Cake washed <bold>a husband</bold>. The husband <bold>surprised</bold> a teacher. The teacher liked " +
#              "homework. The homework <bold>didn't cut</bold> water! The water <bold>grabbed</bold> an uncle. <bold" +
#              ">The uncle</bold> <bold>didn't use</bold> her<bold>.</bold> <bold>She</bold> didn't draw <bold>ice c" +
#              "ream</bold><bold>.</bold> <bold>The ice cream</bold> got a cow<bold>!</bold> <bold>The cow</bold> sa" +
#              "w <bold>lightning</bold>! The lightning grabbed babies<bold>.</bold> <bold>The babies</bold> didn't " +
#              "cook an apple. The apple brought the homework <bold>a leaf</bold>. The leaf made gold out of apple j" +
#              "uice. The apple juice hit the water with a nose. The nose arrested her. -- error count: 13")
#         ]
#         past_error = [
#             ("A tree bought witch, the witches didn't throw fish at an egg! The egg didn't interest an uncle. The " +
#              "uncle didn't hate a child, the child didn't own us. We didn't sell me, i sells a baby to an apple. T" +
#              "he apple interest pens! The pen showed the person a watch, the watch didn't wear an orange. An orang" +
#              "e didn't bite him, he wore poop! Poops surprised a teacher, the teacher loved wives, the wives made " +
#              "noses!"),
#             ("A sand showed him a tree, the tree didn't cook a house. The house smelled a table! The table loved a" +
#              " banana. The banana ate a tiger! The tiger hits her, she surprised you. You built it. It surprised a" +
#              " teacher, the teacher didn't jump on a leaf. The leaf got a pen, the pen didn't fight an egg, the eg" +
#              "g didn't hit us, we rode rices, the rice didn't love her."),
#             ("He stole baby, the baby hit homework with an apple. Apple didn't freeze a table, the table disgusted" +
#              " money. A money hate her. She taught hair a school, the school throws a tiger at oranges! The orange" +
#              "s don't shake the school. The school played with gold. A gold brought a nose to a tree! The tree bui" +
#              "lds a teacher. The teacher bored homeworks! The homework loved the gold! Golds don't see eagles. The" +
#              " eagles taught shark an uncle."),
#             ("Cake washed husbands. The husband surprise a teacher. The teacher liked homework. The homework don't" +
#              " cut water! The water grab an uncle. Uncle doesn't use her, she didn't draw an ice cream, the ice cr" +
#              "eam got a cow, the cow saw a lightning! The lightning grabbed babies, the babies didn't cook an appl" +
#              "e. The apple brought the homework leaf. The leaf made gold out of apple juice. The apple juice hit t" +
#              "he water with a nose. The nose arrested her.")
#         ]
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_paragraph_size(self):
#         random.seed(100)
#         present, past = generate_text(paragraph_size=2)
#
#         present_answer = [
#             "It doesn't wash lightning. The lightning sees a teacher. -- error count: 0",
#             "Thunder picks up eagles. The eagles make <bold>poop</bold> out of cows. -- error count: 1",
#             "Thunder smells <bold>lightning</bold>. The lightning doesn't shake <bold>sand</bold>. -- error count: 2",
#             ("We <bold>disgust</bold> them<bold>.</bold> <bold>They</bold> hate <bold>a child</bold><bold>!</bold>" +
#              " -- error count: 4")
#         ]
#         present_error = [
#             "It doesn't wash lightning. The lightning sees a teacher.",
#             "Thunder picks up eagles. The eagles make a poop out of cows.",
#             "Thunder smells lightnings. The lightning doesn't shake a sand.",
#             "We disgusts them, they hate a childs,"
#         ]
#         past_answer = [
#             "It didn't wash lightning. The lightning saw <bold>a teacher</bold>. -- error count: 1",
#             "Thunder picked up eagles. The eagles made poop out of cows. -- error count: 0",
#             "Thunder didn't smell lightning. The lightning shook sand. -- error count: 0",
#             "We <bold>didn't disgust</bold> them. They <bold>hated</bold> a child! -- error count: 2",
#         ]
#         past_error = [
#             "It didn't wash lightning. The lightning saw teacher.",
#             "Thunder picked up eagles. The eagles made poop out of cows.",
#             "Thunder didn't smell lightning. The lightning shook sand.",
#             "We don't disgust them. They hate a child!"
#         ]
#
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_num_paragraphs(self):
#         random.seed(5)
#         present, past = generate_text(num_paragraphs=2, paragraph_size=1)
#
#         present_answer = ['Money <bold>gets</bold> tea! -- error count: 1',
#                           'Milk disgusts <bold>eagles</bold>. -- error count: 1']
#         present_error = ['Money getted tea!', 'Milk disgusts eagle.']
#         past_answer = ['Money got <bold>tea</bold><bold>!</bold> -- error count: 2',
#                        "Milk <bold>didn't disgust</bold> <bold>eagles</bold>. -- error count: 2"]
#         past_error = ['Money got a tea,', "Milk don't disgust eagle."]
#
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_subject_pool(self):
#         random.seed(50)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=5, subject_pool=1)
#
#         present_answer = [
#             ("A house gives a fire fighter poop. The house brings a finger a book<bold>.</bold> <bold>The house</b" +
#              "old> doesn't get an octopus. The house doesn't draw her! The house throws cake. -- error count: 1")
#         ]
#         present_error = [
#             ("A house gives a fire fighter poop. The house brings a finger a book, the house doesn't get an octopu" +
#              "s. The house doesn't draw her! The house throws cake.")
#         ]
#         past_answer = [
#             ("A house <bold>gave</bold> a fire fighter poop. The house didn't bring <bold>a finger</bold> a book. " +
#              "The house got an octopus. The house didn't draw her! <bold>The house</bold> threw <bold>cake</bold>." +
#              " -- error count: 4")
#         ]
#         past_error = [
#             ("A house give a fire fighter poop. The house didn't bring fingers a book. The house got an octopus. T" +
#              "he house didn't draw her! House threw cakes.")
#         ]
#
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_p_pronoun_one(self):
#         random.seed(215)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=1.0)
#         # The second object is never a pronoun
#         present_answer = ['She brings him to a baby! -- error count: 0']
#         present_error = ['She brings him to a baby!']
#         past_answer = ['She <bold>brought</bold> him to a baby! -- error count: 1']
#         past_error = ['She brings him to a baby!']
#
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_p_pronoun_zero(self):
#         random.seed(2000)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0)
#
#         present_answer = ["Poop interests tea. -- error count: 0"]
#         present_error = ["Poop interests tea."]
#         past_answer = ["Poop didn't interest tea. -- error count: 0"]
#         past_error = ["Poop didn't interest tea."]
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_p_pronoun_some(self):
#         random.seed(2105)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.5)
#
#         present_answer = ["She <bold>steals</bold> <bold>water</bold>. -- error count: 2"]
#         present_error = ["She steal waters."]
#         past_answer = ["She <bold>stole</bold> water. -- error count: 1"]
#         past_error = ["She steals water."]
#         self.assertEqual(present[0], present_answer)
#         self.assertEqual(present[1], present_error)
#         self.assertEqual(past[0], past_answer)
#         self.assertEqual(past[1], past_error)
#
#     def test_p_plural(self):
#         empty = 'tests/test_files/empty.csv'
#         random.seed(123)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=1.0,
#                                       uncountable_file=empty)
#         self.assertEqual(present[0][0], "<bold>Books</bold> shake boxes. -- error count: 1")
#
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=0.0,
#                                       uncountable_file=empty)
#         self.assertEqual(present[0][0], "A box throws a child. -- error count: 0")
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_pronoun=0.0, p_plural=0.65,
#                                       uncountable_file=empty)
#
#         self.assertEqual(present[0][0], "A leaf <bold>arrests</bold> teachers. -- error count: 1")
#
#     def test_p_negative(self):
#         random.seed(123)
#         present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=1.0)
#         self.assertEqual(present[0],
#                          ["I don't shake <bold>a box</bold><bold>.</bold> -- error count: 2",
#                           "We <bold>don't grab</bold> her! -- error count: 1"])
#         self.assertEqual(past[0],
#                          ["I didn't shake a box. -- error count: 0",
#                           "We <bold>didn't grab</bold> her! -- error count: 1"])
#
#         present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=0.0)
#         self.assertEqual(present[0],
#                          ['A sheep steals him. -- error count: 0',
#                           'Tea jumps on <bold>a pineapple</bold>. -- error count: 1'])
#         self.assertEqual(past[0],
#                          ['A sheep <bold>stole</bold> him. -- error count: 1',
#                           'Tea jumped on <bold>a pineapple</bold>. -- error count: 1'])
#
#         present, past = generate_text(num_paragraphs=2, paragraph_size=1, p_negative=0.5)
#         self.assertEqual(present[0],
#                          ['<bold>An apple</bold> <bold>cuts</bold> tea with an ant. -- error count: 2',
#                           "He doesn't bang <bold>octopuses</bold>! -- error count: 1"])
#         self.assertEqual(past[0],
#                          ['An apple cut tea with an ant<bold>.</bold> -- error count: 1',
#                           "He <bold>didn't bang</bold> octopuses! -- error count: 1"])
#
#     def test_p_error(self):
#         random.seed(5613)
#
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0)
#         answer = "<bold>A baby</bold> <bold>brings</bold> them <bold>sand</bold><bold>.</bold> -- error count: 4"
#         self.assertEqual(present[0][0], answer)
#         self.assertEqual(present[1][0], "Baby bringed them sands,")
#         answer = "<bold>A baby</bold> <bold>didn't bring</bold> them <bold>sand</bold><bold>.</bold> -- error count: 4"
#         self.assertEqual(past[0][0], answer)
#         self.assertEqual(past[1][0], "Baby doesn't bring them a sand,")
#
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=0.0)
#         self.assertEqual(present[0][0], "You feed babies. -- error count: 0")
#         self.assertEqual(present[1][0], "You feed babies.")
#         self.assertEqual(past[0][0], "You fed babies. -- error count: 0")
#         self.assertEqual(past[1][0], "You fed babies.")
#
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=0.5)
#         self.assertEqual(present[0][0],
#                          "He <bold>doesn't take</bold> <bold>a fire fighter</bold><bold>.</bold> -- error count: 3")
#         self.assertEqual(present[1][0], "He don't take fire fighter,")
#         self.assertEqual(past[0][0], "He took <bold>a fire fighter</bold><bold>.</bold> -- error count: 2")
#         self.assertEqual(past[1][0], "He took fire fighter,")
#
#     def test_noun_errors(self):
#         random.seed(4589)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0, p_pronoun=0.0,
#                                       noun_errors=True,
#                                       verb_errors=False, period_errors=False)
#         self.assertEqual(present[0][0], "<bold>Octopuses</bold> fight <bold>husbands</bold>. -- error count: 2")
#         self.assertEqual(present[1][0], "Octopus fight husband.")
#         self.assertEqual(past[0][0], "<bold>Octopuses</bold> fought <bold>husbands</bold>. -- error count: 2")
#         self.assertEqual(past[1][0], "The octopus fought a husband.")
#
#     def test_verb_errors(self):
#         random.seed(456132)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=1, p_error=1.0, p_pronoun=0.0,
#                                       verb_errors=True,
#                                       noun_errors=False, period_errors=False)
#         self.assertEqual(present[0][0], "Tigers <bold>pull</bold> pineapples! -- error count: 1")
#         self.assertEqual(present[1][0], "Tigers pulls pineapples!")
#         self.assertEqual(past[0][0], "Tigers <bold>didn't pull</bold> pineapples! -- error count: 1")
#         self.assertEqual(past[1][0], "Tigers don't pull pineapples!")
#
#     def test_period_errors(self):
#         random.seed(4561)
#         present, past = generate_text(num_paragraphs=1, paragraph_size=2, p_error=1.0, p_pronoun=0.0,
#                                       period_errors=True,
#                                       noun_errors=False, verb_errors=False)
#         answer = "A table loves hair<bold>.</bold> <bold>The hair</bold> has a fish<bold>.</bold> -- error count: 2"
#         self.assertEqual(present[0][0], answer)
#         self.assertEqual(present[1][0], "A table loves hair, the hair has a fish,")
#         answer = ("A table loved hair<bold>.</bold> <bold>The hair</bold> didn't have a fish<bold>.</bold> -- " +
#                   "error count: 2")
#         self.assertEqual(past[0][0], answer)
#         self.assertEqual(past[1][0], "A table loved hair, the hair didn't have a fish,")
#
#     def test_verb_file(self):
#         random.seed(459821)
#         file_name = 'tests/test_files/bring.csv'
#         present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, verb_file=file_name)
#         brings = ['Witches bring husbands sand.', 'We bring husbands homework!', 'We bring gold eggs.',
#                   'Cows bring stinky tofu bananas!', "Stinky tofu doesn't bring tea boxes."]
#         broughts = ['Witches brought husbands sand.', 'We brought husbands homework!', "We didn't bring gold eggs.",
#                     'Cows brought stinky tofu bananas!', "Stinky tofu didn't bring tea boxes."]
#         self.assertEqual(present[1], brings)
#         self.assertEqual(past[1], broughts)
#
#     def test_countable_file(self):
#         random.seed(9871)
#         file_name = 'tests/test_files/two_nouns.csv'
#         empty = 'tests/test_files/empty.csv'
#         present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, p_pronoun=0.0,
#                                       countable_file=file_name, uncountable_file=empty)
#         self.assertEqual(present[1],
#                          ["Bobs don't kill joes!", 'Joes see a bob!', 'A joe pulls a bob!', 'Bobs kill joes!',
#                           'A joe draws a bob.'])
#
#     def test_uncountable_file(self):
#         random.seed(4591)
#         file_name = 'tests/test_files/two_nouns.csv'
#         empty = 'tests/test_files/empty.csv'
#         present, past = generate_text(num_paragraphs=5, paragraph_size=1, p_error=0.0, p_pronoun=0.0,
#                                       countable_file=empty, uncountable_file=file_name)
#         # Uncountable nouns don't "s", "a", "an"
#         self.assertEqual(present[1],
#                          ["Joe doesn't take bob.", 'Joe sleeps on bob.', 'Bob cuts joe.', 'Joe bores bob.',
#                           'Joe freezes bob.'])
