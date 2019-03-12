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
                as'4
                b'1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r1
                r1
            }
        >>
    }
}