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
                as'2
                b'2
                c''2
                d''8
                as'2
                ef''2
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r1
                ef'4
                gf'8
                r2
            }
        >>
    }
}