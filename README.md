# SocketTurnBasedTest
Simple mockup of turn based combat using sockets to network between clients

I've just learned about sockets a few weeks ago and studied for a bit, rebuilding a threaded chat client and more to get a feel for them. While there's some obvious errors here and some poor workarounds for things I clearly can't conceptualize yet (there's a use of time.sleep() in the server so the client can run a few print functions and whatnot before it's set to recv(), for instance), I'm within my first week or two of working with sockets and actually using threading.

I figured this would be a good project as it was something A- I knew was within my skill level and B- could be done in a few days. The turn based stuff was gonna just be lifted from my Amulet Engine but for one, that system is deeply ingrained into AmEn, and second, it would be total overkill for a project that was about sockets and networking. So this "game" isn't fun, I know- it's the lousiest turn based combat, but it's all I needed for this. (Though I do intend to patch it up so that the client and server both read 'attacks.py' and create lists of the functions, thus an additional attack added to that file will show up in the game on re-run without any code needing to be added to the client/server, as that was something I wanted to do in AmEn that I never got around to, and it would be a good trick to figure out just in general).


## ISSUES ##
since this is a test and not a full-fledged attempt at creating a working game or tool, there will be some errors here and there, most noticably with iOS and the use of 'input()' instead of 'raw_input()'. But, if you're still using iOS for programming, that's your own fault. 

