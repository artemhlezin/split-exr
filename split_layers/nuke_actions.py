import nuke



def split_explicit(node, layers, alpha, unpremult_all, merge_all, postage_stamp, mirror):

    if mirror:
        mirror = -1
    else:
        mirror = 1
    x_shift = 34

    prev_node = node

    # Dot
    current_node = nuke.nodes.Dot(xpos=prev_node.xpos() + x_shift, ypos=prev_node.ypos() + 150)
    current_node.connectInput(0, prev_node)
    prev_node = current_node

    # Alpha dot, left
    if merge_all:
        alpha_dot1 = nuke.nodes.Dot(xpos=prev_node.xpos() - (200*mirror), ypos=prev_node.ypos())
        alpha_dot1.connectInput(0, prev_node)

    # Unpremult
    if unpremult_all:
        current_node = nuke.nodes.Unpremult(alpha=alpha, channels='all')
        current_node.connectInput(0, prev_node)
        prev_node = current_node

    # Dot
    if unpremult_all:
        current_node = nuke.nodes.Dot(xpos=prev_node.xpos() + x_shift, ypos=prev_node.ypos() + 75)
    else:
        current_node = nuke.nodes.Dot(xpos=prev_node.xpos(), ypos=prev_node.ypos() + 75)
    current_node.connectInput(0, prev_node)
    fork_node = current_node
    prev_node = current_node

    # Shuffle
    current_node = nuke.nodes.Shuffle2(xpos=prev_node.xpos() - x_shift, ypos=prev_node.ypos() + 75)
    current_node.connectInput(0, prev_node)
    current_node.knob('in1').setValue(layers[0])
    current_node.knob('label').setValue('[value in]')
    current_node.knob('postage_stamp').setValue(postage_stamp)
    prev_node = current_node

    # Last nodes
    last_nodes = []
    last_nodes.append(current_node)
    # Back to fork
    current_node = fork_node
    prev_node = current_node

    for i in layers[1:]:
        # Dot to right
        current_node = nuke.nodes.Dot(xpos=prev_node.xpos() + (200*mirror), ypos=prev_node.ypos())
        current_node.connectInput(0, prev_node)
        fork_node = current_node
        prev_node = current_node

        # Shuffle
        current_node = nuke.nodes.Shuffle2(xpos=prev_node.xpos() - x_shift, ypos=prev_node.ypos() + 75)
        current_node.connectInput(0, prev_node)
        current_node.knob('in1').setValue(i)
        current_node.knob('label').setValue('[value in]')
        current_node.knob('postage_stamp').setValue(postage_stamp)
        prev_node = current_node
        last_nodes.append(current_node)
        prev_node = current_node
        prev_node = fork_node

    # Merge
    if not merge_all:
        return True
    else:
        prev_node = last_nodes[0]
        for n, i in enumerate(last_nodes):
            if n < len(last_nodes) - 1:
                current_node = nuke.nodes.Merge2(xpos=prev_node.xpos(), ypos=prev_node.ypos() + 75)
                current_node.knob('operation').setValue('plus')
                current_node.knob('output').setValue('rgb')
                d = nuke.nodes.Dot(xpos=last_nodes[n + 1].xpos() + x_shift, ypos=current_node.ypos() + 4)
                d.setInput(0, last_nodes[n + 1])
                current_node.setInput(0, prev_node)
                current_node.setInput(1, d)
                prev_node = current_node

        # Copy
        current_node = nuke.nodes.Copy(xpos=prev_node.xpos(), ypos=prev_node.ypos() + 150)
        current_node.knob('from0').setValue(alpha)
        current_node.knob('to0').setValue('a')
        alpha_dot2 = nuke.nodes.Dot(xpos=alpha_dot1.xpos(), ypos=current_node.ypos() - 4)
        alpha_dot2.connectInput(0, alpha_dot1)
        current_node.setInput(0, prev_node)
        current_node.setInput(1, alpha_dot2)
        prev_node = current_node

        # Premult
        if unpremult_all:
            current_node = nuke.nodes.Premult(channels='all')
            current_node.connectInput(0, prev_node)
            current_node.autoplace()
            prev_node = current_node

        # Keep rgba
        current_node = nuke.nodes.Remove()
        current_node.connectInput(0, prev_node)
        current_node.autoplace()
        current_node.knob('operation').setValue('keep')
        current_node.knob('channels').setValue('rgba')

        prev_node = current_node


def split_implicit(node, layers):
    prev_node = node

    # Dot
    current_node = nuke.nodes.Dot(xpos=prev_node.xpos() + 34, ypos=prev_node.ypos() + 150)
    current_node.connectInput(0, prev_node)
    prev_node = current_node

    # Merge
    current_node = nuke.nodes.Merge2()
    current_node.autoplace()
    current_node.knob('operation').setValue('plus')
    current_node.knob('output').setValue('rgb')
    current_node.knob('Achannels').setValue('none')
    current_node.knob('Bchannels').setValue(layers[0])
    current_node.knob('label').setValue('[value Bchannels]+[value Achannels]')
    current_node.setInput(0, prev_node)
    current_node.setInput(1, prev_node)
    prev_node = current_node

    for i in layers[1:]:
        current_node = nuke.nodes.Merge2()
        current_node.autoplace()
        current_node.knob('operation').setValue('plus')
        current_node.knob('output').setValue('rgb')
        current_node.knob('Achannels').setValue('rgba')
        current_node.knob('Bchannels').setValue(i)
        current_node.knob('label').setValue('[value Bchannels]+[value Achannels]')
        current_node.setInput(0, prev_node)
        current_node.setInput(1, prev_node)
        prev_node = current_node