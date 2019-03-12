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
                c'2
                gf'16
                r1
                c'2
                f'16
                gf'8
            }
        >>
    }
}