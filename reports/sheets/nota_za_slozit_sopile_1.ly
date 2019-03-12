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
                ef''8
                d''8
                d''2
                b'8
                c''8
                as'16
                b'4
                r4
                b'4
                r1
                c''8
                b'1
                c''8
                d''4
                ef''2
                as'4
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                gf'8
                r1
                f'16
                r2
                ef'4
                r1
                c'8
                b2
                b1
                d'1
                f'4
            }
        >>
    }
}