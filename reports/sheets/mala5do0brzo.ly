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
                gss'2
                ef''8
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r2
                gf'8
            }
        >>
    }
}