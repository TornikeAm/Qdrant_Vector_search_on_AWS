import streamlit as st
import numpy as np
from inference import inf
import numpy as np


def generate_additional_row(image=None, backend_image_path=None, text=None, time=None, res=None, heading=None, url=None,is_initial_row=False):
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="ატვირთული სურათი", use_column_width=True, clamp=True)
    with col2:
        # st.write(backend_image_path)
        backend_image = inf.download_image_from_s3(backend_image_path)
        st.image(backend_image, caption="მსგავსი სურათი", use_column_width=True, clamp=True)

    if is_initial_row:
        with st.container():
            st.write(heading)
            st.write("---")
            st.write(text)
            st.write("---")
            st.write(f"მსგავსების კოეფიციენტი: {res}")
            st.write(f"თარიღი: {time}")
            st.write(f"წყარო: https://mtavari.tv{url}")
    elif not is_initial_row:
        st.write("---")
        st.write(heading)
        with st.expander(label=f"დააკლიკეთ უფრო მეტი ინფორმაციისთვის"):
            st.write(text)
            st.write("---")
            st.write(f"მსგავსების კოეფიციენტი: {res}")
            st.write(f"თარიღი: {time}")
            st.write(f"წყარო: https://mtavari.tv{url}")

def about_page():
    st.title("ჩვენს შესახებ")
    st.write("ყალბი სურათის დეტექტორი ინფორმაციას იღებს შემდეგი ოფიციალური წყაროებიდან")
    points = [
        "მთავარი არხი",
        "იმედი",
        "პირველი არხი",
        "რუსთავი 2",
        "ფორმულა",
        "ტვ პირველი"
    ]

    for point in points:
        st.write(f"* {point}")

def main():
    st.title("Fake Image Detector")

    st.sidebar.header("Navigation")
    st.sidebar.markdown("---")
    page_selection = st.sidebar.radio("", ["მთავარი", "ჩვენს შესახებ"])

    if page_selection == "მთავარი":
        st.header("ატვირთეთ სურათი")

        uploaded_file_main = st.file_uploader("Choose the main image...", type="png")

        if uploaded_file_main is not None:
            st.markdown("---")

            result = inf.get_results(uploaded_file_main)
            num_additional_rows = len(result)

            generate_additional_row(
                uploaded_file_main,
                result[0].payload["time"],
                result[0].payload["text"],
                result[0].payload["time"],
                result[0].score,
                result[0].payload["heading"],
                result[0].payload["href"],
                is_initial_row=True
            )
            if result[0].score < 0.95:
                for i in range(1, num_additional_rows):
                    generate_additional_row(
                        uploaded_file_main,
                        result[i].payload["time"],
                        result[i].payload["text"],
                        result[i].payload["time"],
                        result[i].score,
                        result[i].payload["heading"],
                        result[i].payload["href"]
                    )

    elif page_selection == "ჩვენს შესახებ":
        about_page()

if __name__ == "__main__":
    main()