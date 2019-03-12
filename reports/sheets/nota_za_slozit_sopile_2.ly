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
                ef''8
                c''2
                d''8
                b'4
                as'4
                b'4
                r4
                as'16
                b'4
                d''4
                ef''4
                r4
                c''1
                d''4
                ef''4
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r16
                ef'8
                r4
                ef'4
                r4
                gf'2
                r2
                gf'4
                r4
                r2
                b1
                d'2
            }
        >>
    }
}