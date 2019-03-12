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
                c''4
                r1
                ef''16
                r1
                c''16
                r1
                ef''8
                r4
                d''16
                r1
                c''4
                r1
                d''2
                r1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                d'4
                r4
                d'4
                ef'4
                r16
                d'4
                c'8
                r8
                b4
                c'4
                d'4
                r16
                d'4
                r16
                d'4
                r16
                c'8
                r8
                d'8
                c'8
                b2
                r8
                c'8
                r8
                b1
                r2
                d'4
                r16
                d'8
                r8
                d'8
                r8
                d'8
                r8
                d'8
                r8
                ef'2
                r16
                f'8
                r16
                d'4
                r16
                d'2
                r8
                d'8
                c'8
                b4
                r4
                c'8
                r8
                b2
                r2
                gf'4
                d'8
                r16
                d'4
                ef'4
                r16
                d'8
                r8
                c'4
                r16
                b2
                d'4
                d'4
                r16
                d'8
                r16
                c'4
                r16
                d'8
                c'4
                b2
                r8
                c'4
                r16
                b1
                r2
                d'8
                r16
                d'4
                r16
                d'4
                d'4
                r16
                d'4
                r16
                ef'2
                r16
                f'4
                r16
                d'4
                r16
                d'2
                r8
                d'8
                c'8
                b4
                c'16
                b4
                r16
                c'4
                r8
                b1
            }
        >>
    }
}