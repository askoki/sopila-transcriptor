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
                ef''8
                d''8
                ef''16
                c''4
                d''8
                b'8
                c''8
                as'8
                b'8
                r4
                as'8
                b'8
                c''4
                d''16
                ef''4
                r4
                c''4
                b'2
                c''16
                b'2
                c''2
                d''4
                ef''4
                as'4
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                gf'8
                r8
                gf'16
                r1
                ef'4
                r4
                gf'4
                r2
                f'2
                r16
                f'2
                r8
                f'2
                r2
                gf'4
                ef'2
            }
        >>
    }
}