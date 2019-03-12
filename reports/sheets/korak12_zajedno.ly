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
                b'1
                c''4
                b'4
                as'4
                b'1
                as'4
                b'4
                as'8
                gss'2
                b'1
                r2
                c''2
                b'1
                c''8
                d''4
                gss'16
                ef''4
                d''16
                c''8
                b'1
                as'8
                gss'2
                b'1
                r4
                c''8
                b'2
                c''4
                ef''2
                b'1
                as'8
                b'4
                as'8
                gss'2
                b'1
                r2
                c''8
                b'4
                c''8
                b'8
                c''1
                ef''8
                c''1
                b'16
                c''4
                b'16
                as'8
                gss'2
                as'4
                b'1
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                d'2
                r8
                d'4
                f'16
                ef'8
                d'4
                r16
                c'8
                r16
                c'2
                d'2
                f'8
                d'8
                c'4
                d'4
                c'8
                b2
                gf'8
                b1
                f'16
                r2
                d'2
                f'8
                d'2
                r8
                d'8
                f'8
                ef'8
                f'2
                r16
                d'4
                r16
                d'2
                c'8
                b2
                gf'16
                c'8
                b1
                r4
                gf'4
                d'2
                ef'4
                gf'2
                ef'16
                b2
                d'2
                r8
                d'8
                r16
                c'4
                d'4
                c'4
                b2
                gf'8
                ef'4
                b1
                r2
                d'8
                f'8
                d'2
                gf'4
                ef'2
                c'16
                gf'8
                d'1
                c'4
                b2
                gf'16
                c'4
                b1
            }
        >>
    }
}