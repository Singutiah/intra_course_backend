
# import spacy
# from spacy.training import Example
# from spacy.util import minibatch, compounding
# from spacy.matcher import Matcher
# from spacy.tokens import Span



# nlp = spacy.load("en_core_web_sm")



# Define the training data as a list of Examples
# training_data = []

# def Train(intents):
    # global nlp
    # for intent, data in intents.items():
        # for pattern in data["patterns"]:
          #   doc = nlp.make_doc(pattern)
            # example = Example.from_dict(doc, {"cats": {intent: 1.0}})
            # training_data.append(example)

    # Initialize the spaCy model and create the pipeline
    # nlp = spacy.blank("en")

    # ner = nlp.create_pipe("ner")
    # nlp.add_pipe("ner", last=True)

    # for intent in intents:
        # ner.add_label(intent)

    # Train the model
    # nlp.begin_training()
    # for i in range(20):
      #   losses = {}
        # batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
        # for batch in batches:
          #   nlp.update(batch, losses=losses, drop=0.5)


# Define the chatbot function
def chatbot(intents, text):
    print("hello")
  #   Train(intents)
    # Define the matcher to find keywords in user input
    # matcher = Matcher(nlp.vocab)
    # for intent, data in intents.items():
      #   for pattern in data["patterns"]:
        #     matcher.add(intent, [[{"LOWER": token.lower()} for token in pattern.split()]])
    # doc = nlp(text)
    # matches = matcher(doc)
    # for intent, start, end in matches:
      #   span = Span(doc, start, end, label=intent)
        # doc.ents = list(doc.ents) + [span]
    # for ent in doc.ents:
      #   if ent.label_ in intents:
        #     return intents[ent.label_]["responses"][0]
    # return "I'm sorry, I don't understand. Can you rephrase?"


# Test the chatbot
# print(chatbot("hello"))
# print(chatbot("goodbye"))
# print(chatbot("Can you help me find a flight?"))