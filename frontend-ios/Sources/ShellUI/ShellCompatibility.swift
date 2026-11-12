import SwiftUI

struct ShellGlassEffectContainer<Content: View>: View {
    var spacing: CGFloat?
    let content: Content

    init(spacing: CGFloat? = nil, @ViewBuilder content: () -> Content) {
        self.spacing = spacing
        self.content = content()
    }

    @ViewBuilder var body: some View {
        if #available(iOS 26, macOS 26, *) {
            GlassEffectContainer(spacing: spacing) { content }
        } else {
            content
        }
    }
}

extension View {
    @ViewBuilder func shellGlassButton(prominent: Bool = false) -> some View {
        if #available(iOS 26, macOS 26, *) {
            if prominent {
                buttonStyle(.glassProminent)
            } else {
                buttonStyle(.glass)
            }
        } else if prominent {
            buttonStyle(.borderedProminent)
        } else {
            buttonStyle(.bordered)
        }
    }

    @ViewBuilder func shellGlassEffectID(_ id: String, in namespace: Namespace.ID) -> some View {
        if #available(iOS 26, macOS 26, *) {
            glassEffectID(id, in: namespace)
        } else {
            self
        }
    }

    @ViewBuilder func shellGlassEffectTransition(reduceMotion: Bool) -> some View {
        if #available(iOS 26, macOS 26, *) {
            glassEffectTransition(reduceMotion ? .identity : .matchedGeometry)
        } else {
            self
        }
    }

    @ViewBuilder func shellSafeAreaBar<Content: View>(
        edge: VerticalEdge, spacing: CGFloat = 0, @ViewBuilder content: () -> Content
    ) -> some View {
        if #available(iOS 26, macOS 26, *) {
            safeAreaBar(edge: edge, spacing: spacing, content: content)
        } else {
            safeAreaInset(edge: edge, spacing: spacing, content: content)
        }
    }

    @ViewBuilder func shellSoftScrollEdge() -> some View {
        if #available(iOS 26, macOS 26, *) {
            scrollEdgeEffectStyle(.soft, for: .top)
        } else {
            self
        }
    }

    @ViewBuilder func shellScrollEdgeHidden(_ hidden: Bool) -> some View {
        if #available(iOS 26, macOS 26, *) {
            scrollEdgeEffectHidden(hidden, for: .top)
        } else {
            self
        }
    }

    @ViewBuilder func shellNavigationSubtitle(_ subtitle: String) -> some View {
        if #available(iOS 26, macOS 26, *) {
            navigationSubtitle(subtitle)
        } else {
            self
        }
    }

    @ViewBuilder func shellViewAligned(anchor: UnitPoint) -> some View {
        if #available(iOS 26, macOS 26, *) {
            scrollTargetBehavior(.viewAligned(limitBehavior: .alwaysByOne, anchor: anchor))
        } else {
            scrollTargetBehavior(.viewAligned(limitBehavior: .always))
        }
    }
}

extension ToolbarContent {
    @ToolbarContentBuilder func shellHiddenSharedBackground() -> some ToolbarContent {
        if #available(iOS 26, macOS 26, *) {
            sharedBackgroundVisibility(.hidden)
        } else {
            self
        }
    }
}
