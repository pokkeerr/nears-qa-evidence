# Rendered parity base vs tip (EN, light). Each action: label-text dump (sorted unique ui_list) of the settled screen + a full screenshot; 48 actions
# TEXT-EQUAL on every snapped screen; pixels: 0 px on 47/49 frames (48 actions + the setup frame) after excluding the status-bar strip (clock differs between the two walks); A35 and A42 (home frame taken ~0.5s after the back from a store, home refresh in flight) differ in pixels but are TEXT-EQUAL, and the same home frame later in the walk (A39, A43) is 0 px
# A44 (global-search results page) is png-only: that page's a11y tree goes stub ~12s after it settles (see bug-semantics-assertion-render-table.log), so no label dump exists for it on either build

pixel diff (threshold>8) with the status-bar strip (top 150px: clock/battery) excluded; bbox of remaining diff
A01                        0 px  bbox=None
A02                        0 px  bbox=None
A03                        0 px  bbox=None
A04                        0 px  bbox=None
A05                        0 px  bbox=None
A06                        0 px  bbox=None
A07                        0 px  bbox=None
A08                        0 px  bbox=None
A09                        0 px  bbox=None
A10                        0 px  bbox=None
A11                        0 px  bbox=None
A12                        0 px  bbox=None
A13                        0 px  bbox=None
A14                        0 px  bbox=None
A15                        0 px  bbox=None
A16                        0 px  bbox=None
A17                        0 px  bbox=None
A18                        0 px  bbox=None
A19                        0 px  bbox=None
A20                        0 px  bbox=None
A21                        0 px  bbox=None
A22                        0 px  bbox=None
A23                        0 px  bbox=None
A24                        0 px  bbox=None
A25                        0 px  bbox=None
A26                        0 px  bbox=None
A27                        0 px  bbox=None
A28                        0 px  bbox=None
A29                        0 px  bbox=None
A30                        0 px  bbox=None
A31                        0 px  bbox=None
A32                        0 px  bbox=None
A33                        0 px  bbox=None
A34                        0 px  bbox=None
A35                   132012 px  bbox=(30, 46, 1344, 2763)
A36                        0 px  bbox=None
A37                        0 px  bbox=None
A38                        0 px  bbox=None
A39                        0 px  bbox=None
A40                        0 px  bbox=None
A41                        0 px  bbox=None
A42                   359017 px  bbox=(30, 46, 1344, 2770)
A43                        0 px  bbox=None
A44                        0 px  bbox=None
A45                        0 px  bbox=None
A46                        0 px  bbox=None
A47                        0 px  bbox=None
A48                        0 px  bbox=None
SETUP-grocery-home         0 px  bbox=None

=== snap parity (label text, pixels)
A01          TEXT-EQUAL  1172px
A02          TEXT-EQUAL  888px
A03          TEXT-EQUAL  888px
A04          TEXT-EQUAL  1035px
A05          TEXT-EQUAL  863px
A06          TEXT-EQUAL  863px
A07          TEXT-EQUAL  1056px
A08          TEXT-EQUAL  1056px
A09          TEXT-EQUAL  772px
A10          TEXT-EQUAL  988px
A11          TEXT-EQUAL  888px
A12          TEXT-EQUAL  630px
A13          TEXT-EQUAL  630px
A14          TEXT-EQUAL  1485px
A15          TEXT-EQUAL  1056px
A16          TEXT-EQUAL  1172px
A17          TEXT-EQUAL  888px
A18          TEXT-EQUAL  888px
A19          TEXT-EQUAL  1292px
A20          TEXT-EQUAL  863px
A21          TEXT-EQUAL  1056px
A22          TEXT-EQUAL  1056px
A23          TEXT-EQUAL  772px
A24          TEXT-EQUAL  0px
A25          TEXT-EQUAL  0px
A26          TEXT-EQUAL  0px
A27          TEXT-EQUAL  0px
A28          TEXT-EQUAL  0px
A29          TEXT-EQUAL  0px
A30          TEXT-EQUAL  0px
A31          TEXT-EQUAL  0px
A32          TEXT-EQUAL  3236px
A33          TEXT-EQUAL  0px
A34          TEXT-EQUAL  3180px
A35          TEXT-EQUAL  134917px
A36          TEXT-EQUAL  3348px
A37          TEXT-EQUAL  3357px
A38          TEXT-EQUAL  3159px
A39          TEXT-EQUAL  2747px
A40          TEXT-EQUAL  2940px
A41          TEXT-EQUAL  2652px
A42          TEXT-EQUAL  361765px
A43          TEXT-EQUAL  2940px
A45          TEXT-EQUAL  3366px
A46          TEXT-EQUAL  3348px
A47          TEXT-EQUAL  3464px
A48          TEXT-EQUAL  3464px
SETUP-grocery-home TEXT-EQUAL  1056px
logcat       TEXT-DIFF   -
