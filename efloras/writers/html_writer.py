"""Write output to an HTML file."""

import html
import re
from collections import defaultdict, deque, namedtuple
from datetime import datetime
from itertools import cycle

from jinja2 import Environment, FileSystemLoader

from ..matchers.matcher import MATCHERS
from ..pylib.family_util import get_flora_ids

# CSS colors -- We use 57 of them so far
CLASSES = [f'c{i}' for i in range(57)]
COLORS = cycle(CLASSES)

Cut = namedtuple('Cut', 'pos open len id end type title')

TRAIT_SUFFIXES = [m['name'] for m in MATCHERS]


def html_writer(args, df):
    """Output the data frame."""
    df = df.fillna('')

    flora_ids = get_flora_ids()
    df['flora_name'] = df['flora_id'].map(flora_ids)

    trait_cols = {c for c in df.columns
                  if c.split('_')[-1] in TRAIT_SUFFIXES}
    trait_cols = {c for c in trait_cols if not re.match(r'[2x]|part', c)}
    trait_cols = sorted(trait_cols)

    df = df.sort_values(by=['family', 'taxon'])

    tags = build_tags()
    colors = {t: next(COLORS) for t in trait_cols}

    df['text'] = df.apply(
        format_text, axis='columns',
        colors=colors, tags=tags, trait_cols=trait_cols)

    for col in trait_cols:
        df[col] = df[col].apply(format_trait)

    trait_headers = [f'<span class="{colors[c]}">{c}</span>'
                     for c in trait_cols]

    env = Environment(
        loader=FileSystemLoader('./efloras/writers/templates'),
        autoescape=True)

    template = env.get_template('html_writer.html').render(
        now=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'),
        traits=trait_cols,
        headers=trait_headers,
        rows=df)
    args.output_file.write(template)
    args.output_file.close()


def format_text(row, tags=None, colors=None, trait_cols=None):
    """Colorize and format the text for HTML."""
    text = row['text']
    cuts = []
    cut_id = 0

    for col in trait_cols:
        title = ' '.join(col.split('_'))
        for trait in row[col]:
            cut_id = append_endpoints(
                cuts, cut_id,
                trait['start'], trait['end'],
                colors[col], title=title)

    for sent in row['part']:
        cut_id = append_endpoints(
            cuts, cut_id, sent['start'], sent['end'], 'bold')

    return insert_markup(text, cuts, tags)


def insert_markup(text, cuts, tags):
    """Insert formatting markup for text highlighting etc."""
    # Extract function here
    stack = deque()
    parts = []

    prev_end = 0
    for cut in sorted(cuts):

        # Add text before the tag
        if cut.pos != prev_end:
            parts.append(html.escape(text[prev_end:cut.pos]))
            prev_end = cut.pos

        # Add an open tag
        if cut.open:
            tag = tags[(cut.type, True)]
            if cut.title:
                tag = tag.replace('>', f' title="{cut.title}">')
            parts.append(tag)       # Add tag to output
            stack.appendleft(cut)   # Prepend open cut to stack

        # Close tags are more complicated. We have to search for the
        # matching open tag on the stack & remove it. We also need to
        # reopen any intervening open tags. All while adding the
        # appropriate close tags.
        else:
            # Find matching open tag while keeping any intervening tags
            for idx in range(len(stack)):
                # Append closing tag to output
                parts.append(tags[(stack[0].type, False)])

                # Is this the open tag we are looking for?
                # Open tags have a negative ID and close tags are positive.
                # This pushes the tags to the correct position for sorted
                if abs(stack[0].id) == cut.id:
                    break
                stack.rotate(-1)
            else:
                raise IndexError('Matching open tag not found in stack.')
            # Get rid of matching open tag
            stack.popleft()

            # Put intervening open tags back on stack & reopen in text
            for _ in range(idx):
                stack.rotate(1)
                parts.append(tags[(stack[0].type, True)])

    # Handle text after the last closing tag
    if prev_end != len(text):
        parts.append(html.escape(text[prev_end:]))

    return ''.join(parts)


def append_endpoints(cuts, cut_id, start, end, tag_type, title=None):
    """
    Append endpoints to the cuts.

    The only interesting point is that open cuts have a negative len and
    matching close cuts have a positive len. This will push the cuts to the
    correct position during a sort. Longer cuts need to surround inner cuts.

    Like so:
    [open_cut(len=-2), open_cut(len=-1), close_cut(len=1), close_cut(len=2)]

    The same logic applies to the ID field. We push later tags outward:
    [open_cut(id=-2), open_cut(id=-1), close_cut(id=1), close_cut(id=2)]
    """
    cut_id += 1  # Absolute value is the ID
    trait_len = end - start

    cuts.append(Cut(
        pos=start,
        open=True,  # Close tags come before open tags
        len=-trait_len,  # Longest tags open first
        id=-cut_id,  # Force an order. Push open tags leftward
        end=end,
        type=tag_type,
        title=title,
    ))

    cuts.append(Cut(
        pos=end,
        open=False,  # Close tags come before open tags
        len=trait_len,  # Longest tags close last
        id=cut_id,  # Force an order. Push close tags rightward
        end=end,
        type=tag_type,
        title=None,
    ))

    return cut_id


def build_tags():
    """
    Make tags for HTML text color highlighting.

    Tag keys are the the CSS class and if it's an open or close tag.
    For example:
        (css_class, is_open) -> <span class="css_class">
        (css_class, not_open) -> </span>
    """
    tags = {
        ('bold', True): '<strong>',
        ('bold', False): '</strong>',
    }

    for color in CLASSES:
        tags[(color, True)] = f'<span class="{color}">'
        tags[(color, False)] = '</span>'

    return tags


def format_trait(cell):
    """Format the traits for HTML."""
    pivot = defaultdict(list)
    for trait in cell:
        for key, value in trait.items():
            if key not in ('start', 'end', 'raw_value'):
                pivot[key].append(value)

    output = []
    for _, data in pivot.items():
        simple = {}
        compound = []
        for datum in data:
            if isinstance(datum, dict):
                fields = []
                for key, value in datum.items():
                    value = str(value)
                    field = f'{key}:&nbsp;{value}'
                    fields.append(field)
                compound.append('<br/>'.join(fields))
            else:
                simple[datum] = 1
        simple = ', '.join(simple)
        compound = '<hr/>'.join(compound)
        output.append('<nr/>'.join([x for x in [simple, compound] if x]))
    return '<hr/>'.join(output)
