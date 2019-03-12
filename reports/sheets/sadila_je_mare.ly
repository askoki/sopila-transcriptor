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
                b'2
                c''4
                as'4
                b'2
                c''4
                as'4
                b'2
                c''1
                b'4
                as'2
                c''4
                b'4
                c''4
                as'4
                b'2
                c''1
                as'8
                b'1
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
                c'2
                gf'8
                c'2
                d'2
                c'2
                d'4
                d'4
                r4
                d'2
                b1
            }
        >>
    }
}