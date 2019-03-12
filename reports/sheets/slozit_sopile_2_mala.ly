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
                d''4
                ef''8
                c''2
                d''4
                b'8
                as'4
                b'4
                r4
                as'8
                b'8
                c''8
                d''8
                ef''4
                r4
                c''1
                d''4
                ef''4
                b'8
                as'16
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                ef'16
                r1
                r4
                ef'8
                r1
                r1
                ef'8
                gf'16
            }
        >>
    }
}