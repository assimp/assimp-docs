.. _ai_animation_system

Using the Animation Data
========================

.. _ai_anims:

Animations
----------

An imported scene may contain zero to n **aiAnimation** entries. An animation in this context is a set
of keyframe sequences where each sequence describes the orientation of a single node in the hierarchy
over a limited time span. Animations of this kind are usually used to animate the skeleton of
a skinned mesh, but there are other uses as well.

An **aiAnimation** has a duration. The duration as well as all time stamps are given in ticks. To get
the correct timing, all time stamps thus have to be divided by aiAnimation::mTicksPerSecond. Beware,
though, that certain combinations of file format and exporter don't always store this information
in the exported file. In this case, mTicksPerSecond is set to 0 to indicate the lack of knowledge.

The **aiAnimation** consists of a series of **aiNodeAnim**. Each bone animation affects a single node in
the node hierarchy only, the name specifying which node is affected. For this node the structure
stores three separate key sequences: a vector key sequence for the position, a quaternion key sequence
for the rotation, and another vector key sequence for the scaling. All 3d data is local to the
coordinate space of the node's parent, which means in the same space as the node's transformation matrix.
There might be cases where animation tracks refer to a non-existent node by their name, but this
should not be the case in your everyday data.

To apply such an animation you need to identify the animation tracks that refer to actual bones
in your mesh. Then for every track:
* Find the keys that lay right before the current anim time.
* Optional: interpolate between these and the following keys.
* Combine the calculated position, rotation, and scaling into a transformation matrix
* Set the affected node's transformation to the calculated matrix.

If you need hints on how to convert to or from quaternions, have a look at the
`Matrix & Quaternion FAQ <http://www.j3d.org/matrix_faq/matrfaq_latest.html>`_. I suggest
using logarithmic interpolation for the scaling keys if you happen to need them - usually, you don't
need them at all.

.. _ai_bones:

Bones
-----

A mesh may have a set of bones in the form of instances from the **aiBone** objects. Bones are a means to deform a mesh
according to the movement of a skeleton. Each bone has a name and a set of vertices on which it has influence.
Its offset matrix declares the transformation needed to transform from mesh space to the local space of this bone.

Using the bones name you can find the corresponding node in the node hierarchy. This node in relation
to the other bones' nodes defines the skeleton of the mesh. Unfortunately, there might also be
nodes that are not used by a bone in the mesh but still affect the pose of the skeleton because
they have child nodes which are bones. So when creating the skeleton hierarchy for a mesh I
suggest the following method:

a. Create a map or a similar container to store which nodes are necessary for
the skeleton. Pre-initialize it for all nodes with a "no".

b. For each bone in the mesh:

    b1. Find the corresponding node in the scene's hierarchy by comparing their names.

    b2. Mark this node as "yes" in the necessityMap.

    b3. Mark all of its parents the same way until you

        1. find the mesh's node or
        2. the parent of the mesh's node.

c. Recursively iterate over the node hierarchy.

c1. If the node is marked as necessary, copy it into the skeleton and check its children.

c2. If the node is marked as not necessary, skip it and do not iterate over its children.


Reasons: you need all the parent nodes to keep the transformation chain intact. For most
file formats and modeling packages, the node hierarchy of the skeleton is either a child
of the mesh node or a sibling of the mesh node but this is by no means a requirement so you shouldn't rely on it.
The node closest to the root node is your skeleton root, from there, you
start copying the hierarchy. You can skip every branch without a node being a bone in the mesh -
that's why the algorithm skips the whole branch if the node is marked as "not necessary".

You should now have a mesh in your engine with a skeleton that is a subset of the imported hierarchy.


Blendshapes
----------

ToDo!
