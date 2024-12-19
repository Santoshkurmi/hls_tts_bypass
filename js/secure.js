(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
    [3480], {
        49633: function(e, t, n) {
            (window.__NEXT_P = window.__NEXT_P || []).push(["/secure-player", function() {
                return n(35197)
            }])
        },
        35197: function(e, t, n) {
            "use strict";
            n.r(t), n.d(t, {
                __N_SSP: function() {
                    return I
                },
                default: function() {
                    return C
                }
            });
            var i = n(85893),
                r = n(67294),
                s = n(45508),
                a = n(77999),
                l = n(96486),
                o = n(39154),
                c = n(23956),
                u = n(96076),
                d = n(89885),
                f = n(73716),
                v = n(4298),
                m = n.n(v),
                p = n(63445),
                h = n.n(p),
                y = n(59417),
                w = n(67814),
                g = n(3751),
                x = n(55678),
                b = n(43704),
                S = n(84082),
                j = n(70789),
                k = (n(68777), n(91328)),
                E = n(49475),
                N = n(7079),
                F = n(42238),
                _ = n.n(F);

            function q(e) {
                var t, n, s = function(e) {
                        var t = C.current;
                        if (h().isSupported()) {
                            var n, i = {};
                            f && (i = {
                                enableWorker: !0,
                                lowLatencyMode: !0,
                                backBufferLength: 90,
                                liveSyncDurationCount: 1.5
                            }), R.current = new(h())(i), R.current.loadSource(e), R.current.attachMedia(t), t.addEventListener("loadeddata", (function() {
                                t.playbackRate = A, t.play().then((function(e) {
                                    M(!0), ne(!1)
                                })).catch((function(e) {
                                    ne(!0)
                                }))
                            })), R.current.on(h().Events.ERROR, (function(t, i) {
                                i.type === h().ErrorTypes.NETWORK_ERROR ? n || q || (n = setTimeout((function() {
                                    je({
                                        target: {
                                            value: e
                                        }
                                    }), n = null
                                }), 5e3)) : (i.type, h().ErrorTypes.MEDIA_ERROR)
                            }))
                        } else {
                            var r, s = (new(_())).getOS();
                            Number(null === s || void 0 === s || null === (r = s.version) || void 0 === r ? void 0 : r.split(".")[0]);
                            "iOS" == (null === s || void 0 === s ? void 0 : s.name) && ye(!0)
                        }
                    },
                    a = e.src,
                    c = e.qualities,
                    u = e.seekBarDisabled,
                    f = e.low_latency_enabled,
                    v = e.isWindowsApp,
                    m = e.isMobile,
                    p = void 0 !== m && m,
                    F = e.disableFluidMode,
                    q = void 0 !== F && F,
                    I = e.onBeforeQualityChange,
                    C = (0, r.useRef)(null),
                    R = (0, r.useRef)(),
                    T = (0, r.useState)(!1),
                    L = T[0],
                    M = T[1],
                    O = (0, r.useState)(!1),
                    B = (O[0], O[1], (0, r.useState)(0)),
                    P = B[0],
                    D = B[1],
                    Q = (0, r.useState)("00:00/00:00"),
                    z = Q[0],
                    Z = Q[1],
                    G = (0, r.useState)(1),
                    A = G[0],
                    W = (G[1], (0, r.useState)(!1)),
                    J = W[0],
                    U = W[1],
                    H = (0, r.useState)(),
                    V = H[0],
                    X = H[1],
                    K = (0, r.useState)(!1),
                    Y = K[0],
                    $ = K[1],
                    ee = (0, r.useState)(!0),
                    te = ee[0],
                    ne = ee[1],
                    ie = (0, r.useState)(0),
                    re = ie[0],
                    se = ie[1],
                    ae = (0, r.useState)(e.selectedQuality),
                    le = ae[0],
                    oe = ae[1],
                    ce = (0, r.useContext)(d.Z),
                    ue = ce.appConfig,
                    de = ce.currentUser,
                    fe = (0, r.useState)(e.selectedVideoFitOption || N.zz[0]),
                    ve = fe[0],
                    me = fe[1],
                    pe = (0, r.useState)(!1),
                    he = pe[0],
                    ye = pe[1],
                    we = (0, g.useTimer)({
                        autoStart: !0,
                        expiryTimestamp: (new Date).setSeconds((new Date).getSeconds() + 5),
                        onExpire: function() {
                            Ee()
                        }
                    }),
                    ge = function() {
                        if (C.current) {
                            ! function() {
                                var e = C.current;
                                if (e && e.buffered && e.buffered.length > 0) {
                                    var t = 100 / e.duration * e.buffered.end(0);
                                    se(t)
                                }
                            }(), $(null === R || void 0 === R ? void 0 : R.liveSyncPosition);
                            var e = 100 / C.current.duration * C.current.currentTime;
                            if (isNaN(e)) D(0), Z("00:00/00:00");
                            else {
                                D(e);
                                var t = new Date(1e3 * C.current.duration).toISOString().substr(11, 8),
                                    n = new Date(1e3 * C.current.currentTime).toISOString().substr(11, 8),
                                    i = Math.floor(C.current.duration / 3600),
                                    r = Math.floor(C.current.currentTime / 3600);
                                if (0 != i)
                                    if (0 != r) Z(n + "/" + t);
                                    else {
                                        var s = n.split(":");
                                        n = s[1] + ":" + s[2], Z(n + "/" + t)
                                    }
                                else {
                                    var a = t.split(":");
                                    if (t = a[1] + ":" + a[2], 0 != r) Z(n + "/" + t);
                                    else {
                                        s = n.split(":");
                                        n = s[1] + ":" + s[2], Z(n + "/" + t)
                                    }
                                }
                            }
                        }
                    };
                (0, r.useEffect)((function() {
                    return document.addEventListener("keydown", xe),
                        function() {
                            R.current && R.current.destroy(), document.removeEventListener("keydown", xe)
                        }
                }), []);
                var xe = function(e) {
                    "INPUT" != e.target.tagName && "Space" == e.code && (Se(), e.preventDefault())
                };
                (0, r.useEffect)((function() {
                    var e = C.current;
                    if (e) {
                        var t = a;
                        return e.addEventListener("timeupdate", ge), le && (t = le.path), s(t),
                            function() {
                                C.current && C.current.removeEventListener("timeupdate", ge)
                            }
                    }
                }), [a, C]);
                var be, Se = function() {
                        C.current.paused ? C.current.play() : C.current.pause(), M(!C.current.paused), ne(!1)
                    },
                    je = function(e) {
                        R.current && R.current.destroy();
                        var t = e.target.value;
                        M(!0);
                        var n = c.find((function(e) {
                            return e.path == t
                        }));
                        if (I && !1 === I(n)) return;
                        oe(n), D(0), s(t), ge()
                    },
                    ke = function() {
                        var e = document.getElementById("hlsplayer");
                        if ((!e || !e.classList.contains("user-active")) && (e.classList.remove("user-inactive"), e.classList.add("user-active"), !we.seconds <= 1)) {
                            var t = (new Date).setSeconds((new Date).getSeconds() + 5);
                            we.restart(t, !0)
                        }
                    },
                    Ee = function() {
                        var e = document.getElementById("hlsplayer");
                        e && (e.classList.remove("user-active"), e.classList.add("user-inactive"))
                    };
                return he ? (0, i.jsxs)("div", {
                    className: "d-flex flex-column justify-content-center align-items-center my-5 pt-4",
                    children: [(0, i.jsx)("div", {
                        className: "mb-4 font-lg",
                        children: "Please download the app to watch this video"
                    }), (0, i.jsx)("a", {
                        href: ue.web_iosurl || "https://apps.apple.com/in/app/my-coaching-by-appx/id1662307591",
                        target: "_blank",
                        rel: "noopener noreferrer",
                        children: (0, i.jsx)("img", {
                            src: "https://appx-static.akamai.net.in/app-store.png",
                            width: 150
                        })
                    })]
                }) : (0, i.jsxs)("div", {
                    id: "hlsplayer",
                    onMouseMove: ke,
                    onTouchStart: ke,
                    className: "h-100",
                    style: {
                        position: "relative"
                    },
                    children: [q && (0, i.jsx)(E.Z, {}), ((0, l.isEmpty)(ue.web_enablewatermarkonvideos) || "0" != ue.web_enablewatermarkonvideos) && de && (0, i.jsx)(o.Z, {}), (0, i.jsxs)("div", {
                        style: {
                            height: q ? "100vh" : "100%"
                        },
                        children: [!te && (null === (t = C.current) || void 0 === t ? void 0 : t.readyState) < 2 && (0, i.jsx)(w.G, {
                            icon: y.IJ7,
                            spin: !0,
                            color: "gray",
                            size: "2x",
                            className: "position-absolute center"
                        }), (0, i.jsx)("video", {
                            id: "hlsvideo",
                            style: {
                                width: "100%",
                                objectFit: null !== (be = ve.value) && void 0 !== be ? be : "contain"
                            },
                            ref: C,
                            poster: "/noposter",
                            autoPlay: !1
                        }), te && (0, i.jsx)(w.G, {
                            icon: y.aQp,
                            size: "3x",
                            className: "position-absolute center opacity-75 cursor-pointer text-gray",
                            onClick: Se
                        }), !te && (0, i.jsxs)("div", {
                            id: "hls-player-video-controls",
                            children: [Y - (null === (n = C.current) || void 0 === n ? void 0 : n.currentTime) > 10 && (0, i.jsxs)(S.Z, {
                                size: "sm",
                                color: "link",
                                className: "text-white",
                                onClick: function() {
                                    C.current.currentTime = Y
                                },
                                children: [(0, i.jsx)(w.G, {
                                    style: {
                                        fontSize: "8px"
                                    },
                                    className: "text-danger me-1",
                                    icon: y.diR
                                }), "Go Live"]
                            }), (0, i.jsxs)("div", {
                                className: "d-flex",
                                children: [!f && (0, i.jsx)("div", {
                                    className: "duration mx-2 font-sm d-md-none text-white",
                                    children: z.split("/")[0]
                                }), !u && (0, i.jsx)(j.Z, {
                                    currentTime: P,
                                    bufferedTime: re,
                                    onTimeChange: function(e) {
                                        var t = C.current.duration * (e.target.value / 100);
                                        C.current.currentTime = t, D(e.target.value)
                                    },
                                    seekBarDisabled: u
                                }), !f && (0, i.jsx)("div", {
                                    className: "duration mx-2 font-sm d-md-none text-white",
                                    children: z.split("/")[1]
                                })]
                            }), (0, i.jsxs)("div", {
                                className: "d-flex align-items-center justify-content-between",
                                children: [(0, i.jsxs)("div", {
                                    className: "d-flex align-items-center",
                                    children: [(0, i.jsx)("div", {
                                        id: "hls-play-pause",
                                        className: "icon",
                                        onClick: Se,
                                        children: (0, i.jsx)(w.G, {
                                            icon: L ? y.XQY : y.zc,
                                            className: ""
                                        })
                                    }), !p && (0, i.jsx)(b.Z, {}), u ? (0, i.jsxs)("div", {
                                        className: "text-white px-2 font-sm mt-1",
                                        children: [(0, i.jsx)(w.G, {
                                            style: {
                                                fontSize: "5px"
                                            },
                                            className: "text-danger me-1 mb-1",
                                            icon: y.diR
                                        }), "LIVE"]
                                    }) : (0, i.jsx)("div", {
                                        className: "ms-2 duration font-sm d-none d-md-block text-white",
                                        children: z
                                    })]
                                }), (0, i.jsxs)("div", {
                                    className: "d-flex align-items-center",
                                    children: [e.toggleChat && (0, i.jsx)("div", {
                                        className: "icon pe-2",
                                        onClick: e.toggleChat,
                                        children: (0, i.jsx)(w.G, {
                                            icon: y.lXL
                                        })
                                    }), (0, i.jsx)("div", {
                                        className: "video-fit-options-selector-div",
                                        children: (0, i.jsx)(N.ZP, {
                                            selectedVideoFitOption: ve,
                                            onVideoFitOptionChange: function(e) {
                                                me(e)
                                            }
                                        })
                                    }), c && le && c.length > 0 && (0, i.jsx)("div", {
                                        className: "quality-div",
                                        children: (0, i.jsx)(k.Z, {
                                            qualities: c,
                                            selectedQuality: le,
                                            onQualityChange: je
                                        })
                                    }), "1" != v && !p && (0, i.jsx)("div", {
                                        className: "icon",
                                        onClick: function() {
                                            var e = document.getElementById("hlsvideo");
                                            document.pictureInPictureElement ? document.exitPictureInPicture() : e.requestPictureInPicture().then((function(t) {
                                                X(!0), e.addEventListener("leavepictureinpicture", (function() {
                                                    X(!1)
                                                }))
                                            })).catch((function(e) {
                                                x.Am.error("Picture in picture mode not supported")
                                            }))
                                        },
                                        children: V ? (0, i.jsx)(w.G, {
                                            icon: y.wyP
                                        }) : (0, i.jsx)("img", {
                                            src: "/icons/pic.svg",
                                            style: {
                                                height: "24px",
                                                width: "24px"
                                            }
                                        })
                                    }), (0, i.jsx)("div", {
                                        id: "hls-full-screen",
                                        className: "icon",
                                        style: p ? {
                                            visibility: "hidden"
                                        } : {},
                                        onClick: function() {
                                            var t = function() {
                                                    document.fullscreenElement ? (U(!0), e.setIsFullScreen && e.setIsFullScreen(!0)) : (U(!1), e.setIsFullScreen && e.setIsFullScreen(!1))
                                                },
                                                n = document.getElementById("hlsplayerwithchat") ? document.getElementById("hlsplayerwithchat") : document.getElementById("hlsplayer"),
                                                i = n.getElementsByTagName("video")[0];
                                            null == (n.requestFullscreen ? n.requestFullscreen() : n.mozRequestFullscreen ? n.mozRequestFullscreen() : n.webkitRequestFullscreen ? n.webkitRequestFullscreen() : n.msRequestFullscreen ? n.msRequestFullscreen() : n.webkitEnterFullScreen ? n.webkitEnterFullScreen() : null) ? (i.requestFullscreen ? i.requestFullscreen() : i.mozRequestFullscreen ? i.mozRequestFullscreen() : i.webkitRequestFullscreen ? i.webkitRequestFullscreen() : i.msRequestFullscreen ? i.msRequestFullscreen() : i.webkitEnterFullScreen && i.webkitEnterFullScreen(), i.addEventListener("fullscreenchange", t)) : n.addEventListener("fullscreenchange", t), screen.orientation.lock && screen.orientation.lock("landscape-primary"), document.fullscreenElement ? (document.exitFullscreen(), screen.orientation.lock && screen.orientation.lock("natural")) : J && n.webkitExitFullScreen && n.webkitExitFullScreen()
                                        },
                                        children: (0, i.jsx)(w.G, {
                                            icon: J ? y.Qj4 : y.TL5
                                        })
                                    })]
                                })]
                            })]
                        })]
                    })]
                })
            }
            var I = !0;

            function C(e) {
                var t = e.token,
                    n = e.urls,
                    o = e.isMobile,
                    v = e.isIos,
                    m = e.quality,
                    p = e.watermark,
                    h = e.isLive,
                    y = e.isPremier,
                    w = e.startDate,
                    g = e.datetime,
                    x = e.gcp_cookie,
                    b = e.ivb6,
                    S = e.enable_adaptivebitrate,
                    j = e.seekBarDisabled,
                    k = e.uhs_version,
                    E = (0, r.useState)(!1),
                    N = E[0],
                    F = E[1],
                    _ = (0, r.useContext)(d.Z),
                    I = (_.currentUser, _.setCurrentUser),
                    C = n.find((function(e) {
                        return e.quality == m
                    }));
                C || (C = n[0]);
                var R = {};
                (0, r.useEffect)((function() {
                    if ("undefined" != typeof localStorage) {
                        var e = localStorage.getItem(u.gm);
                        (0, l.isEmpty)(e) || (e = JSON.parse(e), I(e));
                        var i = localStorage.getItem(u.bW);
                        i = i ? JSON.parse(i) : {}, Object.keys(i).filter((function(e) {
                            return e.length > 10
                        })).forEach((function(e) {
                            e != t && delete i[e]
                        })), localStorage.setItem(u.bW, JSON.stringify(i))
                    }
                    if (!(0, l.isEmpty)(x)) {
                        var r = new Date;
                        r.setTime(r.getTime() + 36e5), (0, f.d8)("Edge-Cache-Cookie", x.replace("Edge-Cache-Cookie=", ""), 3600, "/", ".akamai.net.in", !0, !1, "None", !0)
                    }
                    if (g && !v) {
                        var a = (0, s.bd)(g, t).toString("base64");
                        window.lv = a, window.ivb6 = b, window.tmpfn = function(e, t, n) {
							console.trace("Tracking tmpfn to get t function call")
                            return (0, s.k1)(e, t, n, g.charAt(g.length - 1))
                        }
                    }
                    var o = 0;
                    if ("undefined" == typeof window.videojs || "undefined" == typeof window.videojsContribQualityLevels) var c = setInterval((function() {
                        "undefined" != typeof window.videojs && "undefined" == typeof window.videojsContribQualityLevels || 30 == o ? (F(!0), clearInterval(c)) : o += 1
                    }), 1e3);
                    else F(!0);
                    return h || v || (n.forEach((function(e) {
                            R[e.path] = e.jstr
                        })), window.keyString = C.kstr, window.MS = R),
                        function() {}
                }), []);
                var T = function(e) {
                    if (!h) {
                        if (v) {
                            var t, n;
                            window.top && window.top.postMessage("qualityChange", "*"), "undefined" != typeof(null === (t = window.webkit) || void 0 === t || null === (n = t.messageHandlers) || void 0 === n ? void 0 : n.iOSInterface) && window.webkit.messageHandlers.iOSInterface.postMessage(JSON.stringify({
                                event: "qualityChange",
                                data: e
                            }));
                            var i = new URL(window.location.href);
                            return i.searchParams.set("quality", e.quality), window.location.href = i.toString(), !1
                        }
                        window.manifestString = e.jstr, window.keyString = e.kstr
                    }
                };
                return N ? (0, i.jsx)("div", {
                    children: h ? (0, i.jsx)(c.Z, {
                        src: C.path,
                        qualities: n,
                        selectedQuality: C,
                        seekBarDisabled: j,
                        low_latency_enabled: !0,
                        isWindowsApp: !1,
                        isMobile: o,
                        disableFluidMode: !0,
                        watermarkText: p
                    }) : v && k >= 2 ? (0, i.jsx)(q, {
                        src: C.path,
                        qualities: n,
                        selectedQuality: C,
                        seekBarDisabled: j,
                        low_latency_enabled: !0,
                        isWindowsApp: !1,
                        isMobile: o,
                        onBeforeQualityChange: T,
                        disableFluidMode: !0
                    }) : (0, i.jsx)(a.Z, {
                        src: C.path,
                        qualities: n,
                        videoId: "undefined" != typeof localStorage && v ? t : null,
                        selectedQuality: C,
                        onBeforeQualityChange: T,
                        isMobile: o,
                        disableFluidMode: !0,
                        isPremier: y,
                        startDate: w,
                        withCredentials: !(0, l.isEmpty)(x),
                        enableAdaptiveBitrate: S,
                        watermarkText: p
                    })
                }) : null
            }
            C.layout = function(e) {
                var t = e.children;
                return (0, i.jsxs)("div", {
                    children: [(0, i.jsx)(m(), {
                        id: "playerLoader",
                        dangerouslySetInnerHTML: {
                            __html: '\n  const loader = document.getElementById("globalLoader");\n  if (loader) {\n    loader.style.display = "block";\n  }'
                        }
                    }), (0, i.jsx)(m(), {
                        strategy: "beforeInteractive",
                        src: "https://cdnjs.cloudflare.com/ajax/libs/videojs-contrib-quality-levels/2.2.0/videojs-contrib-quality-levels.min.js"
                    }), t]
                })
            }, C.layoutTeachcode = function(e) {
                var t = e.children;
                return (0, i.jsx)("div", {
                    style: {
                        maxHeight: "100%"
                    },
                    className: "overflow-hidden",
                    children: t
                })
            }
        }
    },
    function(e) {
        e.O(0, [9412, 2238, 2480, 6410, 3956, 1453, 9774, 2888, 179], (function() {
            return t = 49633, e(e.s = t);
            var t
        }));
        var t = e.O();
        _N_E = t
    }
]);