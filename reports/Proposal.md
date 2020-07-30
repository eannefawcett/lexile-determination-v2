# Background

In my days as a teacher, reading was encouraged in my classroom, both by myself as the instructor to the students, but also from my supervisors to myself and fellow teachers. We were encouraged to incorporate reading into our content, no matter the content. While I taught chemistry and forensic science in Dallas, the majority of my high school students were on a second grade reading level. Most of the reading materials developed for high school content were on a high school reading level, and inappropriate to ask my students to read if I desired them to be successful. I had to guess at the reading level of content that I found that might be appropriate for my students. It is my goal to create an app that will allow the user to pass in material of any word length, and return an estimated lexile and/or grade level.

# Data Collection

I will first use webscrapping to obtain full texts of popular, open-source children's books. Then, using a different database, I will, using the title, use webscrapping to obtain the lexile level of the text. The texts that I can acquire lexiles for will become my labeled data, against which I will test my unsupervised learning model.

# Data Processing

Next, the obtained full texts will be parsed by book, by chapter, by paragraph, by sentence, by phrase, and by word. These features will be used to engineer new features, along with some other text processing, including using some of the work done by the python nlp library TextBlob.

# Modeling

I haven't decided yet if I will create my own unsupervised learning algorithm for obtaining vector data, or use a pre-trained vector, like GloVe, or some combination of the two.

# Validating the Modeling

I do plan to use the lexiles obtained while webscrapping to validate the trained model.

# Deployment

I plan to use flask to generate a site utilizing the trained model allowing users to directly interact with my work.
