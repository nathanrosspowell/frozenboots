source: "http://github.com/nathanrosspowell/nathanrosspowell.github.com/blob/dev/website/pages/blog/2013/02/17/erlang.md"
named: "erlang"
title: "Erlang"
published: "2013/02/17"
time: "20:13:17"
w3c: "2013-02-17T20:13:17-04:00"
url: "blog/2013/02/17/erlang"
comments: True
short: "Feeling functional, so I added Erlang to the supported functions in my Project Euler codebase"
tags:
- blog
- project-euler

I was feeling functional, so I added [Erlang][erlang] to the supported functions in my Project Euler codebase. While I have done some functional programming already, there are a few features in Erlang that I have never seem before (atoms, etc).
I'm scrolling through [Learn You Some Erlang For Great Good!][leanu] which is in the same vein as the Haskell publication.

    :::erlang
    -module(e0001).
    -export([start/0]).

    start() ->
        Result = lists:sum([ X || X <- lists:seq( 1, 999 ), (X rem 3 =:= 0) or (X rem 5 =:= 0) ]),
        io:fwrite("~w", [Result]).

[erlang]: http://erlang.org
[leanu]: http://learnyousomeerlang.com/
