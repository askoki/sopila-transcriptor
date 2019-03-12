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
                d''8
                r1
                d''2
                r1
                c''4
                r1
                c''16
                r1
                d''8
                r1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                b2
                c'2
                b2
                c'2
                d'1
                ef'4
                c'1
                d'2
                c'2
                d'2
                r2
                d'2
                b1
            }
        >>
    }
}