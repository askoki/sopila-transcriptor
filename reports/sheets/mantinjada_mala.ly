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
                ef''8
                c''4
                b'4
                gss'8
                as'4
                r4
                gss'8
                as'8
                b'8
                c''8
                ef''16
                d''8
                r4
                b'2
                r16
                b'1
                c''4
                d''4
                ef''8
                r2
                ef''8
                c''8
                b'8
                as'8
                gss'4
                as'8
                b'4
                r16
                c''1
                r8
                c''1
                as'2
                c''4
                as'4
                c''4
                as'8
                r8
                c''8
                b'8
                c''4
                as'8
                b'8
                as'8
                gss'8
                as'8
                b'8
                c''8
                d''8
                ef''2
                r4
                c''2
                as'2
                c''8
                b'8
                c''4
                as'4
                b'4
                as'4
                b'8
                gss'8
                b'2
            }
            \context Voice = "vela voice"
            {
                \voiceTwo
                r4
                gf'8
                r1
                gf'8
                r1
                gf'4
                r1
                f'16
                r1
                r1
                gf'16
                r1
            }
        >>
    }
}