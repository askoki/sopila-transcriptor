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
                gss'4
                b'2
                c''4
                d''2
                ef''2
                d''4
                c''2
                b'4
                as'4
                gss'4
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                b4
                d'2
                ef'4
                f'2
                gf'4
                f'4
                ef'4
                d'2
                c'4
                f'16
                b4
            }
        >>
    }
}