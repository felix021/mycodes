Theses code are retrieved from the percy++ project on sourceforge
    http://sourceforge.net/projects/percy/
which is an implementation of the private information retrieval (PIR)
protocols from the paper:

    Ian Goldberg.  Improving the Robustness of Private Information
    Retrieval.  Proc. of 2007 IEEE Symposium on Security and Privacy
    (Oakland 2007), May 2007.

Goldberg himself is the owner of that project.

recover.cc contains only the findpoly algorithm, which adopts the interpolation
algorithm proposed by Sudan, and the Roth-Ruckenstein algorithm(rr\_roots.cc) 
for finding roots.

Shamely, I can't get this to work, since the NTL library is very hard to use :(

What's more, this is retrieved from the 0.6 version, since the project replaced
GS algorithm with a more efficient one in ver 0.7
