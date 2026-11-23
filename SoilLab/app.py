                "Filter-pack D30 / aquifer D30 ratio",
                [4, 5, 6],
                index=[4, 5, 6].index(suggested),
                help=f"Suggested ratio for this formation category: {suggested}.",
            )
        with i3:
            target_cu = st.number_input(
                "Target filter-pack Cu",
                min_value=1.01,
                max_value=2.50,
                value=2.00,
                step=0.05,
            )

        if params["D30"] is None:
            st.error("Aquifer D30 cannot be determined from the current data.")
        else:
            try:
                pack_curve, pack = design_filter_pack(params["D30"], factor, target_cu)

                st.divider()
                st.subheader("Proposed filter-pack properties")
                pcols = st.columns(4)
                pcols[0].metric("Filter-pack D10", f'{pack["D10"]:.3f} mm')
                pcols[1].metric("Filter-pack D30", f'{pack["D30"]:.3f} mm')
                pcols[2].metric("Filter-pack D60", f'{pack["D60"]:.3f} mm')
                pcols[3].metric("Filter-pack Cu", f'{pack["Cu"]:.2f}')

                st.info(
                    f"**D30 (filter pack)** = {factor} × D30 (aquifer) = "
                    f"{factor} × {params['D30']:.3f} mm = **{pack['D30']:.3f} mm**."
                )
                st.metric(
                    "Preliminary maximum screen-opening check",
                    f'{pack["D10"]:.3f} mm',
                    help="Preliminary retention check only. Final screen design requires additional checks.",
                )

                st.subheader("Gradation curves")
                draw_gradation_curve(results, pack_curve, "Aquifer and Proposed Filter-Pack Gradation")

                st.subheader("Proposed filter-pack data")
                st.dataframe(
                    pack_curve.iloc[::15].rename(columns={
                        "particle_size_mm": "Particle size (mm)",
                        "percent_passing": "Percentage passing (%)",
                    }),
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Particle size (mm)": st.column_config.NumberColumn(format="%.4f"),
                        "Percentage passing (%)": st.column_config.NumberColumn(format="%.2f"),
                    },
                )
                st.warning(
                    "This smooth curve is a theoretical lognormal grading target, not a tested gravel product. "
                    "Laboratory-test the actual filter-pack material and verify retention, permeability, "
                    "bridging, placement and screen compatibility."
                )
            except ValueError as exc:
                st.error(str(exc))

# ============================================================
# SETTINGS AND HELP
# ============================================================
elif page == "Settings & Help":
    st.header("Settings & Help")

    st.subheader("Appearance")
    st.write("Choose the visual theme that is most comfortable for your working environment.")
    selected_theme = st.radio(
        "Application theme",
        ["Light", "Dark"],
        index=0 if st.session_state["appearance"] == "Light" else 1,
        horizontal=True,
        key="settings_appearance",
    )
    if selected_theme != st.session_state["appearance"]:
        st.session_state["appearance"] = selected_theme
        st.rerun()
    st.caption("The selected theme applies to the interface and gradation graph for this session.")

    st.divider()
    st.subheader("Desmos graph setup")
    st.markdown("""
    1. Obtain a Desmos Graphing Calculator API key from [Desmos API](https://www.desmos.com/my-api).
    2. Enter the key in the **Desmos Graph** section of the left sidebar.
    3. Open **Sieve Analysis** or **Filter-Pack Design** to view the interactive grading curve.

    The graph plots log₁₀(particle size in mm) horizontally and percentage passing vertically.
    This is the standard semi-logarithmic grading-curve arrangement. The measured points are
    connected in ascending particle-size order without spline smoothing.
    """)

    st.divider()
    st.subheader("How to use SoilLab")
    st.markdown("""
1. Enter sieve openings in **mm** and retained dry mass in **g**, or upload an Excel workbook.
2. Enter the total dry sample mass.
3. Calculate the sieve analysis and check mass recovery.
4. Review D10, D30, D40, D60, D70, Cu and Cc.
5. Open **Automatic Well Selection** and choose the formation condition based on the bore log.
6. If gravel packing is selected, use **Filter-Pack Design** to generate a preliminary grading curve.
""")

    st.divider()
    st.subheader("Design assumptions and limitations")
    st.markdown("""
- The automatic well recommendation uses preliminary criteria supplied in the user's lecture slides.
- The current interpretation uses a natural-well slot interval of 0.40 × D40 to 0.70 × D70.
- The gravel-pack trigger uses homogeneous / uniform formation, Cu < 3 and D10 < 0.25 mm, or an interpreted upper slot estimate below 0.75 mm.
- Filter-pack D30 is selected at 4, 5 or 6 times aquifer D30; target filter-pack Cu is limited to 2.5.
- The filter-pack curve is theoretical. Actual pack material must be tested by sieve analysis.
- Do not combine different aquifer strata into one averaged curve.
- Final design must consider aquifer stability, fines migration, screen retention, open area, entrance velocity, corrosion, structural strength, well development and manufacturer tolerances.
""")

st.divider()
st.caption("SoilLab · Particle and sieve sizes: mm · Mass: g · Percentages: % · Preliminary design support only.")
