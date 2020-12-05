import re

from liir.dame.core.io.CoNLL2005Writer import write_short_conll2005_format
from liir.dame.core.io.TextReader import TextReader
from liir.dame.core.representation.Predicate import Predicate
from liir.dame.core.representation.Sentence import Sentence
from liir.dame.core.representation.Text import Text
from liir.dame.core.representation.Word import Word

__author__ = "Quynh Do"
__copyright__ = "Copyright 2017, DAME"


class CoNLL2005Reader(TextReader):
    def __init__(self, sources, predicate_pos=2, entity_pos=1):  # 5):
        TextReader.__init__(self, sources)
        self.predicate_pos = predicate_pos
        self.entity_pos = entity_pos

    def read_file(self, fn):
        f = open(fn, "r", encoding="utf-8")
        sentences = []
        words = []
        for line in f.readlines():
            line = line.strip()
            if re.match("\\s+", line) or line == "":
                if len(words) > 0:
                    sentences.append(words)
                    words = []
            else:
                words.append(line)

        f.close()
        if len(words) > 0:
            sentences.append(words)

        txt = Text()
        for lines in sentences:
            txt.append(self.generate_sentence(lines))
        return txt

    def generate_sentence(self, lines):
        pred_id = 0

        dt = []
        sen = Sentence()
        for line in lines:
            temps = re.split("\\s+", line)
            dt.append(temps)
            w = Word(temps[0])

            if w.is_numeric():
                w.form = "**NUM**"

            if temps[self.predicate_pos] != "-":
                w = Predicate(w)
                w.lemma = temps[self.predicate_pos]

            sen.append(w)

        # read srl information
        for pred in sen:
            if isinstance(pred, Predicate):
                args = self.get_args(pred, lines, dt, pred_id)
                pred.arguments = args
                pred_id += 1

        # assign entity tag
        j = 0
        while j < len(lines):
            tmps = dt[j]
            label = tmps[self.entity_pos]
            match = re.match('\((.+)\*\)', label)
            if match:
                sen[j].entity_tag = "B-" + match.group(1)
                j += 1
            else:
                match = re.match("\((.+)\*", label)
                if match:
                    sen[j].entity_tag = "B-" + match.group(1)
                    for k in range(j + 1, len(lines)):
                        sen[k].entity_tag = "I-" + match.group(1)
                        tmps1 = dt[k]
                        match_inside = re.match('\*\)', tmps1[self.entity_pos])
                        if match_inside:
                            j = k + 1
                            break
                else:
                    sen[j].entity_tag = "O"
                    j += 1
        return sen

    def get_args(self, pred, lines, dt, pred_id):
        args = []
        j = 0
        while j < len(lines):
            tmps = dt[j]
            lbl = tmps[1 + self.predicate_pos + pred_id]
            match = re.match('\((.+)\*\)', lbl)
            if match:
                args.append("B-" + match.group(1))
                j += 1
            else:
                match = re.match('\((.+)\*', lbl)
                if match:
                    args.append("B-" + match.group(1))
                    for k in range(j + 1, len(lines)):
                        args.append("I-" + match.group(1))
                        l1 = lines[k]
                        tmps1 = re.split("\\s+", l1)
                        match1 = re.match('\*\)', tmps1[1 + self.predicate_pos + pred_id])
                        if match1:
                            j = k + 1
                            break
                else:
                    args.append("O")
                    j += 1
        return args

if __name__=="__main__":
    import sys
    data_file = sys.argv[1]
    #output = sys.argv[2]
    reader = CoNLL2005Reader(data_file, predicate_pos=2)
    txt = reader.read_all()
    for sen in txt:
        for w in sen:
            print(w)
    #write_short_conll2005_format(reader.read_all(), output)