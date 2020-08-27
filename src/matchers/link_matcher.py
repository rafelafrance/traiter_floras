"""Base matcher object."""

from collections import defaultdict

from traiter.trait_matcher import TraitMatcher

from .attach import ATTACH
from ..pylib.util import LINK_STEP

MATCHERS = [ATTACH]


class LinkMatcher(TraitMatcher):
    """Base matcher object."""

    name = 'entity_matcher'

    def __init__(self, nlp):
        super().__init__(nlp)
        links = TraitMatcher.step_rules(MATCHERS, LINK_STEP)
        self.add_patterns(links, LINK_STEP)

        # This is used for sorting matches
        self.priority = {m['label']: m.get('priority', 9999) for m in links}
        for action in self.actions:
            label = action.split('.')[0]
            self.priority[action] = self.priority[label]

    def filter_matches(self, matches):
        """Remove overlapping matches following priority rules."""
        strings = self.nlp.vocab.strings

        # Group matches by priority
        priorities = defaultdict(list)
        for match in matches:
            label = strings[match[0]]
            priority = self.priority[label]
            priorities[priority].append(match)

        # Order matches in each list by longest then leftmost
        for priority, match_list in priorities.items():
            priorities[priority] = sorted(
                match_list, key=lambda m: (m[1] - m[2], m[1]))

        # Build list by adding longest matches w/ no overlap by priority
        matches = []
        for priority in sorted(priorities.keys()):
            match_list = priorities[priority]
            for match in match_list:
                for prev in matches:
                    if (prev[1] <= match[1] < prev[2]
                            or prev[1] < match[2] <= prev[2]):
                        break
                else:
                    matches.append(match)

        return matches

    def scan(self, doc, matchers, step):
        """Find all terms in the text and return the resulting doc."""
        all_matches = []

        for matcher in matchers:
            all_matches += matcher(doc)

        for sent in doc.sents:
            matches = [m for m in all_matches
                       if m[1] >= sent.start and m[2] <= sent.end]
            matches = self.filter_matches(matches)

            part = [t for t in sent if t.ent_type_ == 'part']
            part = part[0] if part else None

            for match_id, start, end in matches:
                span = doc[start:end]
                label = self.nlp.vocab.strings[match_id]
                if action := self.actions.get(label):
                    action(span, part)

        return doc
