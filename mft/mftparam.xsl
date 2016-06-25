<xsl:stylesheet
    version="1.0"
    xmlns:src="http://mftsomethingnamespace" 
    xmlns="http://mftsomethingnamespace"   
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:namespace-alias stylesheet-prefix="src" result-prefix=""/>
	
	<xsl:param name="contentfolder" />
	
	<xsl:template match="/src:root/src:attribute[@name='Content Folder']/src:replace">
	<src:replace><xsl:value-of select="$contentfolder"/></src:replace>
	</xsl:template>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>

</xsl:stylesheet>
