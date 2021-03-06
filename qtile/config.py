# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import psutil

mod = "mod4"
terminal = "kitty"
scrotout = "scrot '~/!BOOKSHELF/Pictures/Screenshots/`date +%Y`/`date +%Y_m`/%F_%T_$wx$h.png"
scrotoutS = "scrot -s '~/!BOOKSHELF/Pictures/Screenshots/`date +%Y`/`date +%Y_m`/%F_%T_$wx$h.png"

scrotclip = "scrot '/tmp/%F_%T_$wx$h.png' -e 'xclip -selection clipboard -target image/png -i $f'"
scrotclipS = "scrot -s '/tmp/%F_%T_$wx$h.png' -e 'xclip -selection clipboard -target image/png -i $f'"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "space", lazy.spawn("rofi -show run"), desc="Spawn the rofi launcher"),

    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +2%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -2%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute toggle")),
   
    Key([], "Print", lazy.spawn(scrotclip)),
    Key(["shift"], "Print", lazy.spawn(scrotclipS)),
    Key([mod], "Print", lazy.spawn(scrotout)),
    Key([mod, "shift"], "Print", lazy.spawn(scrotoutS)),

    # Chords
    KeyChord([mod], "x", [
		Key(["shift"], "w", lazy.layout.grow_up()),
		Key(["shift"], "a", lazy.layout.grow_left()),
		Key(["shift"], "s", lazy.layout.grow_down()),
		Key(["shift"], "d", lazy.layout.grow_right()),
		Key([], "Up", lazy.layout.up()),
		Key([], "Left", lazy.layout.left()),
		Key([], "Down", lazy.layout.down()),
		Key([], "Right", lazy.layout.right()),
		Key([], "w", lazy.layout.shuffle_up()),
		Key([], "a", lazy.layout.shuffle_left()),
		Key([], "s", lazy.layout.shuffle_down()),
		Key([], "d", lazy.layout.shuffle_right()),
		Key([], "x", lazy.window.kill()),
		Key([], "space", lazy.spawn(terminal))
		],mode="Window"
	)
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            )
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Bsp(
	border_focus='000000',
	border_normal='bebebe',
	border_on_single=True,
	border_width=2,
	margin=12
	),
    #layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Monoid",
    fontsize=12,
    padding=4,
)
extension_defaults = widget_defaults.copy()

separator = widget.Sep(padding=10, size_percent=25, foreground='bebebe')

screens = [
    Screen(
	# wallpaper = '~/Pictures/Wallpapers/Angewandt_Layers_Background_light_2.png',
	# wallpaper_mode = 'stretch', 
        top = bar.Bar(
            [
                widget.GroupBox(
				this_screen_border = '000000',
				this_current_screen_border = '000000',
				active = '000000',
				block_highlight_text_color = 'e6e6e6',
				foreground = '000000',
				highlight_method = "block", 
				hide_unused = True,
				margin_x = 2,
				padding_x = 12,
				rounded = False,
				),
                widget.TaskList(
				border = '000000',
				unfocused_border = 'bebebe',
				active = '000000',
				block_highlight_text_color = 'e6e6e6',
				foreground='e6e6e6',
				highlight_method = "block",
				margin = 2,
				padding_x = 24,
				rounded = False,
				icon_size = 0
				),
                widget.Chord(
		    background = 'ff0000',
		    foreground = '000000',
                    chords_colors={
                        "launch": ("#ff0000", "#000000"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Prompt(foreground = '000000'),
		widget.Moc(play_color = '500050', noplay_color = '000000'),
		separator,
		widget.Memory(foreground = '005000', format='{MemUsed:.0f}{mm}'),
		separator,
		widget.CPU(foreground = '000050', format='{load_percent}%'),
		separator,
                widget.Volume(foreground = '500000', fmt='VOL {}'),
		separator,
		widget.Wttr(foreground = '505000', location = {'Duluth' : 'Duluth'}, units = 'u', format = '%t'),
		separator,
		widget.Systray(),
		separator,
                widget.Clock(format="%a %b %d, %Y @ %H:%M:%S", foreground="#000000"),
            ],
            28,
	    background = 'e6e6e6',
            border_width=[0, 0, 2, 0],  # Draw top and bottom borders
            border_color=["bebebe", "bebebe", "bebebe", "bebebe"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
