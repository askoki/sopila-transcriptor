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
                ef''8
                r1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                b4
                c'2
                d'2
                ef'2
                gf'1
            }
        >>
    }
}