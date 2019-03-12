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
                as'4
                b'1
                c''2
                ef''1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r2
                gf'2
                r16
                f'8
                r4
                gf'1
                r16
                ef'16
                r16
                ef'8
                r8
            }
        >>
    }
}