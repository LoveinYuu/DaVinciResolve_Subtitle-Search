# Author: Yuu
# Version: 1.1

ui = fusion.UIManager
disp = bmd.UIDispatcher(ui)

Search_Box = 'Search_Box'
Search_Button = 'Search_Button'
Sub_Tree = 'Sub_Tree'
Go_To = 'Go_To'


def project():
    pjM = resolve.GetProjectManager()
    pj = pjM.GetCurrentProject()
    return pj


def frames_to_timecode(frames):
    framerate = project().GetSetting('timelineFrameRate')
    return '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600*framerate)),
                                                    int(frames / (60*framerate) % 60),
                                                    int(frames / framerate % 60),
                                                    int(frames % framerate))


def load_subtitle():
    tl = project().GetCurrentTimeline()
    sub_list = []
    track_item_list = tl.GetItemListInTrack('subtitle', 1)
    for i in track_item_list:
        sub_list.append(frames_to_timecode(i.GetStart()) + '    ' + i.GetName())
    return sub_list


def search(ev):
    itm[Sub_Tree].Clear()
    target = itm[Search_Box].Text
    sub_list = load_subtitle()
    top_level_items = []
    for i in sub_list:
        if target in i:
            row = itm[Sub_Tree].NewItem()
            row.Text[0] = i
            top_level_items.append(row)
    itm[Sub_Tree].AddTopLevelItems(top_level_items)


def goto(ev):
    tl = project().GetCurrentTimeline()
    timecode = itm[Sub_Tree].CurrentItem().Text[0][0:12]
    tl.SetCurrentTimecode(timecode)


def _exit(ev):
    disp.ExitLoop()


main_window = ui.VGroup([
    ui.HGroup({'Spacing': 5, 'Weight': 0, 'StyleSheet': 'max-height: 25px'}, [
        ui.Label({'Text': '🔎', 'Weight': 0}),
        ui.LineEdit({'ID': Search_Box, 'PlaceholderText': 'Type in text here...'}),
        ui.Button({'ID': Search_Button, 'Text': 'Search', 'Weight': 0})
    ]),
    ui.Tree({'ID': Sub_Tree, 'AlternatingRowColors': True, 'HeaderHidden': True, 'SelectionMode': 'ExtendedSelection',
             'Weight': 2}),
    ui.HGroup({'StyleSheet': 'max-height: 25px'}, [
        ui.Button({'ID': Go_To, 'Text': 'GoTo'})
    ]),
])

dlg = disp.AddWindow({
    "WindowTitle": "Subtitle Search V1.1",
    "ID": "Subtitle_Search",
    "Geometry": [
        400, 800,
        400, 300
    ],
},
    main_window)

itm = dlg.GetItems()

dlg.On[Search_Button].Clicked = search
dlg.On[Go_To].Clicked = goto

dlg.On.Subtitle_Search.Close = _exit
dlg.Show()
disp.RunLoop()
dlg.Hide()
