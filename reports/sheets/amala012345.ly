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
                ef''2
                d''2
                c''2
                b'2
                as'2
                gss'1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r1
            }
        >>
    }
}