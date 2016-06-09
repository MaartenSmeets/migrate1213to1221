<xsl:stylesheet
    version="1.0"
    xmlns:src="http://maven.apache.org/POM/4.0.0" 
    xmlns="http://maven.apache.org/POM/4.0.0"   
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:namespace-alias stylesheet-prefix="src" result-prefix=""/>

	<xsl:template match="/src:project/src:parent"/>

	<xsl:template match="/src:project/src:packaging[text()='sbar']">
		<src:packaging>jar</src:packaging>
	</xsl:template>

	<xsl:template match="@*|node()">
		<xsl:copy>
			<xsl:apply-templates select="@*|node()"/>
		</xsl:copy>
	</xsl:template>
</xsl:stylesheet>
