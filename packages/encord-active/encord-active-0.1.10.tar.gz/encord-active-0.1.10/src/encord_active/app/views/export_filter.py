from datetime import datetime
from typing import Tuple, cast

import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
)

import encord_active.app.common.state as state
from encord_active.app.common.action_utils import create_new_project_on_encord_platform
from encord_active.app.common.utils import load_merged_df, set_page_config, setup_page
from encord_active.app.db.tags import Tags


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let apps filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    with st.container():
        columns_to_filter = df.columns.to_list()
        if "url" in columns_to_filter:
            columns_to_filter.remove("url")
        # Move tags to first option.
        tags_column = columns_to_filter.pop(columns_to_filter.index("tags"))
        columns_to_filter = [tags_column] + columns_to_filter

        to_filter_columns = st.multiselect("Filter dataframe on", columns_to_filter)
        if to_filter_columns:
            df = df.copy()

        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            key = f"filter-select-{column.replace(' ', '_').lower()}"

            if column == "tags":
                tag_filters = right.multiselect("Choose tags to filter", options=Tags().all(), key=key)
                filtered_rows = [True if set(tag_filters) <= set(x) else False for x in df["tags"]]
                df = df.loc[filtered_rows]

            # Treat columns with < 10 unique values as categorical
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                if df[column].isnull().sum() != df.shape[0]:
                    user_cat_input = right.multiselect(
                        f"Values for {column}",
                        df[column].unique(),
                        default=list(df[column].unique()),
                        key=key,
                    )
                    df = df[df[column].isin(user_cat_input)]
                else:
                    right.markdown(f"For column *{column}*, all values are NaN")
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                    key=key,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                first = df[column].min()
                last = df[column].max()
                res = right.date_input(
                    f"Values for {column}", min_value=first, max_value=last, value=(first, last), key=key
                )
                if isinstance(res, tuple) and len(res) == 2:
                    res = cast(Tuple[pd.Timestamp, pd.Timestamp], map(pd.to_datetime, res))  # type: ignore
                    start_date, end_date = res
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                    key=key,
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def export_filter():
    setup_page()
    message_placeholder = st.empty()

    st.markdown("# Actions")

    load_merged_df()
    filtered_df = filter_dataframe(st.session_state[state.MERGED_DATAFRAME].copy())
    filtered_df.reset_index(inplace=True)
    st.subheader("Filter & Export")
    st.markdown(f"**Total row:** {filtered_df.shape[0]}")
    st.dataframe(filtered_df, use_container_width=True)

    action_columns = st.columns((5, 2, 2, 2))
    action_columns[0].download_button(
        "⬇ Download filtered data",
        filtered_df.to_csv(index=False).encode("utf-8"),
        file_name=f"Encord Active Data {datetime.now().strftime('%Y_%m_%d %H_%M_%S')}.csv",
    )
    delete_btn = action_columns[1].button("❌ Delete")
    edit_btn = action_columns[2].button("🖋 Edit")
    augment_btn = action_columns[3].button("➕ Augment")

    if any([delete_btn, edit_btn, augment_btn]):
        message_placeholder.markdown(
            """
<div class="encord-active-info-box">
    🛠️ We're working hard on this feature - but not quite there yet.
    Please get in touch with Encord on the
    <a href="https://encordactive.slack.com" target="_blank"><i class="fa-brands fa-slack"></i> Encord Active Slack 
community</a>
    or shoot us an
    <a href="mailto:support@encord.com" target="_blank"><i class="fa fa-envelope"></i> email</a> for more information 
and help 🙏
</div>
""",
            unsafe_allow_html=True,
        )

    with st.expander("Create a new project with the selected items"):
        l_column, r_column = st.columns(2)

        dataset_title = l_column.text_input(
            "Dataset title", value=f"Subset: {st.session_state.project_dir.name} ({filtered_df.shape[0]})"
        )
        dataset_description = l_column.text_area("Dataset description")

        project_title = r_column.text_input(
            "Project title", value=f"Sub-project: {st.session_state.project_dir.name} ({filtered_df.shape[0]})"
        )
        project_description = r_column.text_area("Project description")

        create_new_project = st.button("➕ Create")
        if create_new_project:
            if dataset_title == "":
                st.error("Dataset title cannot be empty!")
                return
            if project_title == "":
                st.error("Project title cannot be empty!")
                return
            create_new_project_on_encord_platform(
                dataset_title, dataset_description, project_title, project_description, filtered_df
            )


if __name__ == "__main__":
    set_page_config()
    export_filter()
