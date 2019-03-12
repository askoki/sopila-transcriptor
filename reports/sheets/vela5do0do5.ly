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
                b2
                c'2
                d'2
                ef'2
                f'2
                d'16
                c'16
                d'4
                d'2
                f'1
                d'2
                c'2
                b4
            }
        >>
    }
}