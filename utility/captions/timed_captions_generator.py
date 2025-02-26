def getCaptionsWithTime(whisper_analysis, maxCaptionSize=15):
    text = whisper_analysis["text"]
    words = text.split()
    captions = []
    current_caption = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= maxCaptionSize:
            current_caption.append(word)
            current_length += len(word) + 1
        else:
            captions.append(" ".join(current_caption))
            current_caption = [word]
            current_length = len(word)
    
    if current_caption:
        captions.append(" ".join(current_caption))

    return captions
