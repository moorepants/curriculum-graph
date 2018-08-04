This script creates a directed graph of the UC Davis Mechanical and Aerospace
Engineering Curriculum.

The data is stored in ``courses.yml`` with the following format::

   ENG 045:
     title: Properties of Materials
     required: EME
     required-choice:
     group: Engineering
     prereqs:
       - MAT 021C or MAT 017C
       - CHE 002A
       - PHY 009A
     variations:
       - Y

Each entry represents a course in the catalog which is specified by the three
character topic string (e.g. EME, EAE, ENG) and a three digit number with an
optional single closing letter. Example valid entries are: ``EME 050``, ``EME 185A``.

The subfields are:

``title``
   A string that holds the title of the course.
``required``
   Comma separated three character major codes that this course is
  a strict requirement of (e.g. ``EAE`` or ``EME, EAE``.
``required-choice``
   Comma separated three character major codes that this course is a
   requirement of (e.g. ``EAE`` or ``EME, EAE``, but that the student can
   choose among a group.
``group``
   The curriculum group this course belongs to.
``prereqs``
   A list of preqequisite courses. These should be the course number
``variations``
   A list of modifiers to the course designator. For example the honors version
   of CHE 002A is CHE 002AH. So ``- H`` would be added to this list.

Install the dependencies with conda::

    $ conda install networkx pygraphviz pyyaml
