# ADB dumpsys package to Pandas DataFrame


```python

$pip install a-pandas-ex-dumpsys-to-df

from a_pandas_ex_dumpsys_to_df import pd_add_dumpsys_to_dataframe
pd_add_dumpsys_to_dataframe()
import pandas as pd
dumpsysdump=(someadbpackage.device.shell(r'dumpsys package'))
df=pd.Q_dumpsys_to_df(dumpsysdump)

                       aa_0             aa_1                                                             aa_2                                                                                    aa_3  aa_4
0   Activity Resolver Table  Full MIME Types                           application/com.google.android.gms.car                                                                                    <NA>  <NA>
1   Activity Resolver Table  Full MIME Types                           application/com.google.android.gms.car                                       5747077 com.google.android.gms/.car.FirstActivity  <NA>
2   Activity Resolver Table  Full MIME Types                                            application/pkix-cert                                                                                    <NA>  <NA>
3   Activity Resolver Table  Full MIME Types                                            application/pkix-cert                                    fe254e4 com.android.certinstaller/.CertInstallerMain  <NA>
4   Activity Resolver Table  Full MIME Types                               vnd.android.cursor.dir/raw_contact                                                                                    <NA>  <NA>
5   Activity Resolver Table  Full MIME Types                               vnd.android.cursor.dir/raw_contact                   593cd4d com.android.contacts/.activities.CompactContactEditorActivity  <NA>
6   Activity Resolver Table  Full MIME Types                               vnd.android.cursor.dir/raw_contact                          f0a1002 com.android.contacts/.activities.ContactEditorActivity  <NA>
7   Activity Resolver Table  Full MIME Types                                     application/x-zip-compressed                                                                                    <NA>  <NA>
8   Activity Resolver Table  Full MIME Types                                     application/x-zip-compressed                                          bb59d13 com.android.documentsui/.FilesActivity  <NA>
9   Activity Resolver Table  Full MIME Types                                       application/x-x509-ca-cert                                                                                    <NA>  <NA>
10  Activity Resolver Table  Full MIME Types                                       application/x-x509-ca-cert                                    fe254e4 com.android.certinstaller/.CertInstallerMain  <NA>
11  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                                                                                    <NA>  <NA>
12  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                               d2a4e com.android.phone/.EmergencyOutgoingCallBroadcaster  <NA>
13  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                                           1e1db50 com.android.dialer/.DialtactsActivity  <NA>
14  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person             37a5905 com.android.contacts/.quickcontact.QuickContactActivity (2 filters)  <NA>
15  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                   593cd4d com.android.contacts/.activities.CompactContactEditorActivity  <NA>
16  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person           6115c7c com.android.contacts/.activities.ContactSelectionActivity (2 filters)  <NA>
17  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                                      ddcf149 com.android.phone/.OutgoingCallBroadcaster  <NA>
18  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                            ed2f76f com.android.phone/.PrivilegedOutgoingCallBroadcaster  <NA>
19  Activity Resolver Table  Full MIME Types                                   vnd.android.cursor.item/person                          f0a1002 com.android.contacts/.activities.ContactEditorActivity  <NA>
20  Activity Resolver Table  Full MIME Types  vnd.android.cursor.item/com.google.android.gms.matchstick.phone                                                                                    <NA>  <NA>
21  Activity Resolver Table  Full MIME Types  vnd.android.cursor.item/com.google.android.gms.matchstick.phone             1159d5a com.google.android.gms/.matchstick.call.ContactsVideoActionActivity  <NA>
22  Activity Resolver Table  Full MIME Types  vnd.android.cursor.item/com.google.android.gms.matchstick.phone   9c19b8b com.google.android.gms/.matchstick.call.ContactsPrivilegedVideoActionActivity  <NA>
23  Activity Resolver Table  Full MIME Types                                                multipart/related                                                                                    <NA>  <NA>
24  Activity Resolver Table  Full MIME Types                                                multipart/related  d55c468 com.android.chrome/com.google.android.apps.chrome.IntentDispatcher (2 filters)  <NA>
25  Activity Resolver Table  Full MIME Types                                                multipart/related      fcc8081 com.android.chrome/org.chromium.chrome.browser.printing.PrintShareActivity  <NA>
26  Activity Resolver Table  Full MIME Types                                                       video/3gpp                                                                                    <NA>  <NA>
27  Activity Resolver Table  Full MIME Types                                                       video/3gpp                                      e003526 com.android.gallery3d/.app.GalleryActivity  <NA>
28  Activity Resolver Table  Full MIME Types                            vnd.android.cursor.dir/postal-address                                                                                    <NA>  <NA>
29  Activity Resolver Table  Full MIME Types                            vnd.android.cursor.dir/postal-address                       6115c7c com.android.contacts/.activities.ContactSelectionActivity  <NA>
30  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/calls                                                                                    <NA>  <NA>
31  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/calls                                           1e1db50 com.android.dialer/.DialtactsActivity  <NA>
32  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/calls                                          7ac6567 com.android.contacts/.NonPhoneActivity  <NA>
33  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/event                                                                                    <NA>  <NA>
34  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/event                                         ff6bf14 com.android.calendar/.EditEventActivity  <NA>
35  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/image                                                                                    <NA>  <NA>
36  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/image                          e003526 com.android.gallery3d/.app.GalleryActivity (3 filters)  <NA>
37  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/phone                                                                                    <NA>  <NA>
38  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/phone                       6115c7c com.android.contacts/.activities.ContactSelectionActivity  <NA>
39  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/video                                                                                    <NA>  <NA>
40  Activity Resolver Table  Full MIME Types                                     vnd.android.cursor.dir/video                          e003526 com.android.gallery3d/.app.GalleryActivity (2 filters)  <NA>
41  Activity Resolver Table  Full MIME Types                                                application/x-zip                                                                                    <NA>  <NA>
42  Activity Resolver Table  Full MIME Types                                                application/x-zip                                          bb59d13 com.android.documentsui/.FilesActivity  <NA>
43  Activity Resolver Table  Full MIME Types                                    application/x-shockwave-flash                                                                                    <NA>  <NA>
44  Activity Resolver Table  Full MIME Types                                    application/x-shockwave-flash                                        7bfa3bd com.android.gallery3d/.app.MovieActivity  <NA>
45  Activity Resolver Table  Full MIME Types                                    application/vnd.wap.xhtml+xml                                                                                    <NA>  <NA>
46  Activity Resolver Table  Full MIME Types                                    application/vnd.wap.xhtml+xml                                      1aa7db2 com.android.htmlviewer/.HTMLViewerActivity  <NA>
47  Activity Resolver Table  Full MIME Types                                                  application/pdf                                                                                    <NA>  <NA>
48  Activity Resolver Table  Full MIME Types                                                  application/pdf                                        18ff103 com.bluestacks.filemanager/.MainActivity  <NA>
49  Activity Resolver Table  Full MIME Types                                                  application/sdp                                                                                    <NA>  <NA>
....

 
```