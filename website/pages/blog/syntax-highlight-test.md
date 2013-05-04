source: "http://github.com/nathanrosspowell/nathanrosspowell.github.com/blob/dev/website/pages/blog/2012/08/04/syntax-highlight-test.md"
named: "syntax-highlight-test"
title: "Syntax Highlight Test"
published: "2012/08/04"
time: "00:44:54"
w3c: "2012-08-04T00:44:54+00:00"
url: "blog/2012/08/04/syntax-highlight-test"
template: "blog_post.html"
comments: True
short: This is the test for code syntax highlighting from markdown source.
tags:
- code
- test
- python
- c++
- basic 

This is the test for code syntax highlighting from markdown source.

Goodbye world in [BASIC][bas]:

    :::basic
    10 PRINT "Goodbye, World!"

Fibonacci sequence in [python][py]:

    :::python
    def fibRec(n):
        if n < 2:
            return n
        else:
            return fibRec(n-1) + fibRec(n-2)

Sieve of Eratosthenes in [C++][cpp]:

    :::c++
    // yield all prime numbers less than limit. 
    template<class UnaryFunction>
    void primesupto(int limit, UnaryFunction yield)
    {
      std::vector<bool> is_prime(limit, true);
     
      const int sqrt_limit = static_cast<int>(std::sqrt(limit));
      for (int n = 2; n <= sqrt_limit; ++n)
        if (is_prime[n]) {
        yield(n);
     
        for (unsigned k = n*n, ulim = static_cast<unsigned>(limit); k < ulim; k += n) 
          //NOTE: "unsigned" is used to avoid an overflow in `k+=n` for `limit` near INT_MAX
          is_prime[k] = false;
        }
     
      for (int n = sqrt_limit + 1; n < limit; ++n)
        if (is_prime[n])
        yield(n);
    }

[bas]: http://rosettacode.org/wiki/Hello_world#BASIC
[py]: http://rosettacode.org/wiki/Fibonacci_sequence#Python
[cpp]: http://rosettacode.org/wiki/Sieve_of_Eratosthenes#C.2B.2B
