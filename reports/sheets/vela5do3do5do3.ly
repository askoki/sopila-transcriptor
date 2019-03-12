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
                b'8
                r1
                ef''8
                b'8
                r4
                ef''8
                r2
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                c'4
                d'8
                ef'2
                d'4
                c'4
                b8
                c'4
                d'8
                ef'4
                f'16
                ef'16
                d'8
                c'4
                b4
            }
        >>
    }
}