\version "2.18.2"
\language "english"

\header {
    tagline = ##f
}

\layout {}

\paper {}

\score {
    \new Staff
    \with
    {
        \remove Time_signature_engraver
        \remove Bar_engraver
    }
    {
        <<
            \context Voice = "mala voice"
            {
                \voiceOne
                r1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                b4
                c'4
                d'4
                r8
                d'4
                c'4
                b4
                r8
                b4
                c'4
                d'4
                r8
                d'4
                c'4
                b4
            }
        >>
    }
}