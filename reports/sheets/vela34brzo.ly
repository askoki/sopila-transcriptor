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
                r8
                d''8
                d''16
                r2
                d''4
                r16
                d''16
                r4
                d''16
                r1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                ef'8
                f'8
                b16
                d'2
                b16
                f'4
                d'16
                b16
                d'4
                b16
                ef'4
                ef'4
                d'16
                ef'8
                ef'8
                ef'8
                ef'4
                ef'16
                d'16
                ef'2
                d'16
            }
        >>
    }
}