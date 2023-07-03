from spanbert import SpanBERT
def spanBertResults(inputFormat):
    spanbert = SpanBERT("./pretrained_spanbert")
    return spanbert.predict(inputFormat)

